from flask import Blueprint, Response, jsonify, request
from back.database import get_db

drones_bp = Blueprint("drones", __name__)

@drones_bp.get("/drones")
def list_drones() -> Response:
    with get_db() as conn:
        rows = conn.execute("""
            Select Drone.id, Drone.name, Drone.status, Drone.is_waterproof, Drone.has_encoder_sd_card, Drone.details, Radio.ip, Radio.mesh, Payload.is_ir_boson_plus
            From Drone
            Left Join Radio on Drone.id_radio = Radio.id
            Left join Payload on Drone.id_payload = Payload.id
            """).fetchall()
        
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