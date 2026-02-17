from __future__ import annotations

import inspect
import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request

from src.Model.GCS import GCS
from src.Model.battery import Battery
from src.Model.drone import Drone
from src.Model.raspberry import Raspberry


app = Flask(__name__)
DB_PATH = Path("resources.db")


MODEL_REGISTRY = {
	"BATTERY": Battery,
	"DRONE": Drone,
	"GCS": GCS,
	"RASPBERRY": Raspberry,
}


def get_db() -> sqlite3.Connection:
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db() -> None:
	conn = get_db()
	conn.execute(
		"""
		CREATE TABLE IF NOT EXISTS resource (
			db_id INTEGER PRIMARY KEY AUTOINCREMENT,
			resource_id TEXT NOT NULL UNIQUE,
			resource_type TEXT NOT NULL,
			name TEXT NOT NULL,
			status INTEGER NOT NULL DEFAULT 0,
			description TEXT,
			attributes TEXT
		)
		"""
	)
	cols = [row[1] for row in conn.execute("PRAGMA table_info(resource)").fetchall()]
	if "status" not in cols:
		conn.execute("ALTER TABLE resource ADD COLUMN status INTEGER NOT NULL DEFAULT 0")
	conn.commit()
	conn.close()


def get_model_spec() -> dict[str, dict[str, Any]]:
	specs: dict[str, dict[str, Any]] = {}
	for type_name, cls in MODEL_REGISTRY.items():
		sig = inspect.signature(cls.__init__)
		fields: list[dict[str, Any]] = []
		for name, param in sig.parameters.items():
			if name in {"self", "resource_id"}:
				continue
			annotation = param.annotation if param.annotation is not inspect._empty else str
			required = param.default is inspect._empty
			fields.append(
				{
					"name": name,
					"type": annotation,
					"required": required,
				}
			)
		specs[type_name] = {"class": cls, "fields": fields}
	return specs


MODEL_SPECS = get_model_spec()


def normalize_type(type_name: str | None) -> str:
	if not type_name:
		raise ValueError("Field 'type' is required.")
	normalized = type_name.upper()
	if normalized not in MODEL_SPECS:
		raise ValueError(f"Unknown resource type '{type_name}'.")
	return normalized


def cast_value(value: Any, expected_type: Any) -> Any:
	if expected_type is bool:
		if isinstance(value, bool):
			return value
		if isinstance(value, str):
			lowered = value.strip().lower()
			if lowered in {"true", "1", "yes", "on"}:
				return True
			if lowered in {"false", "0", "no", "off"}:
				return False
		if isinstance(value, (int, float)):
			return bool(value)
		raise ValueError("Expected a boolean value.")

	if expected_type is int:
		if isinstance(value, bool):
			raise ValueError("Expected an integer, got boolean.")
		return int(value)

	if expected_type is float:
		if isinstance(value, bool):
			raise ValueError("Expected a float, got boolean.")
		return float(value)

	return str(value) if value is not None else ""


def validate_status(value: Any) -> int:
	status_val = cast_value(value, int)
	if status_val not in {0, 1, 2}:
		raise ValueError("Field 'status' must be 0, 1 or 2.")
	return status_val


def validate_payload(payload: dict[str, Any], resource_type: str, partial: bool = False) -> dict[str, Any]:
	spec = MODEL_SPECS[resource_type]["fields"]
	allowed = {f["name"]: f for f in spec}

	if "name" not in allowed:
		raise ValueError("Model must include a 'name' field in constructor.")

	submitted_attrs = payload.get("attributes")
	if submitted_attrs is None:
		submitted_attrs = {}
	if not isinstance(submitted_attrs, dict):
		raise ValueError("Field 'attributes' must be an object.")

	unknown = [k for k in submitted_attrs if k not in allowed or k in {"name", "description", "status"}]
	if unknown:
		raise ValueError(f"Unknown attribute(s) for type {resource_type}: {', '.join(unknown)}")

	result: dict[str, Any] = {}
	for f in spec:
		field_name = f["name"]
		field_type = f["type"]
		required = f["required"]

		if field_name in {"name", "description", "status"}:
			if field_name in payload:
				if field_name == "status":
					result[field_name] = validate_status(payload[field_name])
				else:
					result[field_name] = cast_value(payload[field_name], field_type)
			elif required and not partial:
				raise ValueError(f"Missing required field '{field_name}'.")
			continue

		if field_name in submitted_attrs:
			result[field_name] = cast_value(submitted_attrs[field_name], field_type)
		elif required and not partial:
			raise ValueError(f"Missing required attribute '{field_name}'.")

	return result


def row_to_resource(row: sqlite3.Row) -> dict[str, Any]:
	attrs_raw = row["attributes"]
	try:
		attrs = json.loads(attrs_raw) if attrs_raw else {}
	except Exception:
		attrs = {}

	return {
		"id": row["resource_id"],
		"type": row["resource_type"],
		"name": row["name"],
		"status": row["status"],
		"description": row["description"] or "",
		"attributes": attrs,
	}


@app.get("/health")
def health() -> Any:
	return jsonify({"status": "ok"})


@app.get("/resource-types")
def resource_types() -> Any:
	result = {}
	for type_name, spec in MODEL_SPECS.items():
		fields = []
		for f in spec["fields"]:
			py_type = f["type"]
			type_label = py_type.__name__ if hasattr(py_type, "__name__") else str(py_type)
			fields.append({"name": f["name"], "type": type_label, "required": f["required"]})
		result[type_name] = fields
	return jsonify(result)


@app.post("/resources")
def create_resource() -> Any:
	payload = request.get_json(silent=True) or {}
	try:
		resource_type = normalize_type(payload.get("type"))
		validated = validate_payload(payload, resource_type, partial=False)
	except ValueError as exc:
		return jsonify({"error": str(exc)}), 400

	resource_id = str(uuid.uuid4())
	name = validated.get("name", "")
	status = validated.get("status", 0)
	description = validated.get("description", "")
	attrs = {k: v for k, v in validated.items() if k not in {"name", "description", "status"}}

	conn = get_db()
	conn.execute(
		"""
		INSERT INTO resource (resource_id, resource_type, name, status, description, attributes)
		VALUES (?, ?, ?, ?, ?, ?)
		""",
		(resource_id, resource_type, name, status, description, json.dumps(attrs) if attrs else None),
	)
	conn.commit()
	row = conn.execute("SELECT * FROM resource WHERE resource_id = ?", (resource_id,)).fetchone()
	conn.close()

	return jsonify(row_to_resource(row)), 201


@app.get("/resources")
def list_resources() -> Any:
	type_filter = request.args.get("type")
	conn = get_db()
	if type_filter:
		try:
			normalized = normalize_type(type_filter)
		except ValueError as exc:
			conn.close()
			return jsonify({"error": str(exc)}), 400
		rows = conn.execute("SELECT * FROM resource WHERE resource_type = ? ORDER BY db_id DESC", (normalized,)).fetchall()
	else:
		rows = conn.execute("SELECT * FROM resource ORDER BY db_id DESC").fetchall()
	conn.close()
	return jsonify([row_to_resource(r) for r in rows])


@app.get("/resources/<string:resource_id>")
def get_resource(resource_id: str) -> Any:
	conn = get_db()
	row = conn.execute("SELECT * FROM resource WHERE resource_id = ?", (resource_id,)).fetchone()
	conn.close()
	if not row:
		return jsonify({"error": "Resource not found."}), 404
	return jsonify(row_to_resource(row))


@app.route("/resources/<string:resource_id>", methods=["PUT", "PATCH"])
def update_resource(resource_id: str) -> Any:
	payload = request.get_json(silent=True) or {}
	conn = get_db()
	row = conn.execute("SELECT * FROM resource WHERE resource_id = ?", (resource_id,)).fetchone()
	if not row:
		conn.close()
		return jsonify({"error": "Resource not found."}), 404

	current = row_to_resource(row)
	is_partial = request.method == "PATCH"

	try:
		new_type = normalize_type(payload.get("type", current["type"]))
		merged_payload = {
			"name": payload.get("name", current["name"]),
			"status": payload.get("status", current["status"]),
			"description": payload.get("description", current["description"]),
			"attributes": current["attributes"].copy(),
		}
		if isinstance(payload.get("attributes"), dict):
			merged_payload["attributes"].update(payload["attributes"])

		validated = validate_payload(merged_payload, new_type, partial=is_partial)
	except ValueError as exc:
		conn.close()
		return jsonify({"error": str(exc)}), 400

	name = validated.get("name", current["name"])
	status = validated.get("status", current["status"])
	description = validated.get("description", current["description"])
	attrs = {k: v for k, v in validated.items() if k not in {"name", "description", "status"}}

	conn.execute(
		"""
		UPDATE resource
		SET resource_type = ?, name = ?, status = ?, description = ?, attributes = ?
		WHERE resource_id = ?
		""",
		(new_type, name, status, description, json.dumps(attrs) if attrs else None, resource_id),
	)
	conn.commit()
	updated = conn.execute("SELECT * FROM resource WHERE resource_id = ?", (resource_id,)).fetchone()
	conn.close()

	return jsonify(row_to_resource(updated))


@app.delete("/resources/<string:resource_id>")
def delete_resource(resource_id: str) -> Any:
	conn = get_db()
	row = conn.execute("SELECT * FROM resource WHERE resource_id = ?", (resource_id,)).fetchone()
	if not row:
		conn.close()
		return jsonify({"error": "Resource not found."}), 404

	conn.execute("DELETE FROM resource WHERE resource_id = ?", (resource_id,))
	conn.commit()
	conn.close()
	return "", 204


if __name__ == "__main__":
	init_db()
	app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
