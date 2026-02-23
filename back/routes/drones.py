from flask import Blueprint, Response, jsonify, request
from back.database import get_db

drones_bp = Blueprint("drones", __name__)

@drones_bp.get("/drones")
def list_resources() -> Response:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM Drone").fetchall()
    
    return jsonify([dict(r) for r in rows])

@drones_bp.get("/drones/<int:id>")
def get_drone(id: int) -> Response:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM Drone WHERE id = ?", (id,)).fetchone()
        
    if row is None:
        return jsonify({"error": "Drone not found"}), 404
    
    return jsonify(dict(row))

@drones_bp.post("/drones")
def create_drone() -> Response:
    body = request.get_json()
    
    if not body or "name" not in body:
        return jsonify({"error": "Missing required field: name"}), 400
    
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO Drone (name, id_radio) VALUES (?, ?)",
            (body["name"], body.get("id_radio"))
        )
        
    return jsonify({"id": cursor.lastrowid}), 201

@drones_bp.delete("/drones/<int:id>")
def delete_drone(id: int) -> Response:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM Drone WHERE id = ?", (id,)).fetchone()        
        if row is None:
            return jsonify({"error": "Drone not found"}), 404
        
        conn.execute("DELETE FROM Drone WHERE id = ?", (id,))        
    return jsonify({"message": "Drone deleted"}), 200