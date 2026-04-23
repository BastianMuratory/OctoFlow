from flask import Blueprint, Response, jsonify, request
from back.database import get_db

drones_bp = Blueprint("drones", __name__)

@drones_bp.get("/drones")
def list_drones() -> Response:
    with get_db() as conn:
        rows = conn.execute("""
            Select Drone.id, Drone.name, Drone.status, Drone.details, Drone.is_waterproof, Drone.has_pix_double_layer_support, Drone.is_c5_c6_compliant, Drone.has_encoder, Drone.has_encoder_sd_card, Drone.encoder_version,
            Radio.ip, Radio.mesh, Radio.model, Radio.is_drone_config, Radio.encryption_type, Radio.encryption_key, Radio.min_frequency, Radio.max_frequency,
            Payload.reverse_mounting, Payload.has_eo, Payload.has_ir, Payload.eo_info, Payload.ir_info, Payload.ir_frequency, Payload.is_ir_boson_plus, Payload.ir_sensitivity
            
            From Drone
            Left Join Radio on Drone.id_radio = Radio.id
            Left join Payload on Drone.id_payload = Payload.id
            """).fetchall()
        
    return jsonify([dict(r) for r in rows])


@drones_bp.delete("/drones/<int:id>")
def delete_drone(id: int) -> Response:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM Drone WHERE id = ?", (id,)).fetchone()
        if row is None:
            return jsonify({"error": "Drone not found"}), 404
        
        conn.execute("DELETE FROM Drone WHERE id = ?", (id,))
    return jsonify({"message": "Drone deleted"}), 200


@drones_bp.put("/drones/<int:id>")
def update_drone(id: int) -> Response:
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing body"}), 400

    with get_db() as conn:
        # Check if drone exist in db
        row = conn.execute("SELECT * FROM Drone WHERE id = ?", (id,)).fetchone()
        if row is None:
            return jsonify({"error": "Drone not found"}), 404

        # Update drone
        conn.execute("""
            UPDATE Drone SET
                status = COALESCE(?, status),
                is_waterproof = COALESCE(?, is_waterproof),
                has_pix_double_layer_support = COALESCE(?, has_pix_double_layer_support),
                is_c5_c6_compliant = COALESCE(?, is_c5_c6_compliant),
                has_encoder = COALESCE(?, has_encoder),
                has_encoder_sd_card = COALESCE(?, has_encoder_sd_card),
                encoder_version = COALESCE(?, encoder_version)
            WHERE id = ?
        """, (
            body.get("status"),
            body.get("waterproof"),
            body.get("pix"),
            body.get("ce"),
            body.get("encoder"),
            body.get("sd"),
            body.get("encoderVersion"),
            id
        ))

        # Update Radio
        conn.execute("""
            UPDATE Radio SET
                ip = COALESCE(?, ip),
                mesh = COALESCE(?, mesh),
                encryption_key = COALESCE(?, encryption_key),
                encryption_type = COALESCE(?, encryption_type),
                model = COALESCE(?, model)
            WHERE id = (SELECT id_radio FROM Drone WHERE id = ?)
        """, (
            body.get("ip"),
            body.get("mesh"),
            body.get("password"),
            body.get("aes"),
            body.get("model"),
            id
        ))

        # Update Payload
        conn.execute("""
            UPDATE Payload SET
                has_eo = COALESCE(?, has_eo),
                has_ir = COALESCE(?, has_ir),
                eo_info = COALESCE(?, eo_info),
                ir_info = COALESCE(?, ir_info),
                reverse_mounting = COALESCE(?, reverse_mounting)
            WHERE id = (SELECT id_payload FROM Drone WHERE id = ?)
        """, (
            body.get("eo"),
            body.get("ir"),
            body.get("eoInfo"),
            body.get("irInfo"),
            body.get("payloadMount"),
            id
        ))

    return jsonify({"message": "Drone updated"}), 200

@drones_bp.get("/drones/<int:id>/flights")
def get_flights(id: int) -> Response:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM Flights WHERE id_drone = ? ORDER BY date DESC", (id,)
        ).fetchall()
        return jsonify([dict(r) for r in rows])

@drones_bp.post("/drones/<int:id>/flights")
def create_flight(id: int) -> Response:
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing body"}), 400
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO Flights (id_drone, date, pilot, duration, purpose, comments)
               VALUES (?, strftime('%s', 'now'), ?, ?, ?, ?)""",
            (id, body.get("pilot"), body.get("duration"), body.get("purpose"), body.get("comments"))
        )
        return jsonify({"id": cursor.lastrowid}), 201
    
@drones_bp.put("/drones/<int:drone_id>/flights/<int:flight_id>")
def update_flight(drone_id: int, flight_id: int) -> Response:
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing body"}), 400

    with get_db() as conn:
        row = conn.execute("SELECT * FROM Flights WHERE id = ? AND id_drone = ?", (flight_id, drone_id)).fetchone()
        if row is None:
            return jsonify({"error": "Flight not found"}), 404

        conn.execute("""
            UPDATE Flights SET
                pilot = COALESCE(?, pilot),
                duration = COALESCE(?, duration),
                purpose = COALESCE(?, purpose),
                comments = COALESCE(?, comments)
            WHERE id = ?
        """, (
            body.get("pilot"),
            body.get("duration"),
            body.get("purpose"),
            body.get("comments"),
            flight_id
        ))

    return jsonify({"message": "Flight updated"}), 200

@drones_bp.get("/drones/<int:id>/operations")
def get_operations(id: int) -> Response:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM Operation WHERE id_drone = ? ORDER BY date DESC", (id,)
        ).fetchall()
        return jsonify([dict(r) for r in rows])

@drones_bp.post("/drones/<int:id>/operations")
def create_operation(id: int) -> Response:
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing body"}), 400
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO Operation (id_drone, date, operation_type, description, made_by, reviewed_by, material_cost, comments)
               VALUES (?, strftime('%s', 'now'), ?, ?, ?, ?, ?, ?)""",
            (id, body.get("type"), body.get("description"), body.get("done_by"),
             body.get("validated_by"), body.get("material_cost") or 0, body.get("comments"))
        )
        return jsonify({"id": cursor.lastrowid}), 201

@drones_bp.put("/drones/<int:drone_id>/operations/<int:operation_id>")
def update_operation(drone_id: int, operation_id: int) -> Response:
    body = request.get_json()
    if not body:
        return jsonify({"error": "Missing body"}), 400
    
    print(body.get("type"), body.get("description"), body.get("done_by"))

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM Operation WHERE id = ? AND id_drone = ?", (operation_id, drone_id)
        ).fetchone()
        if row is None:
            return jsonify({"error": "Operation not found"}), 404

        conn.execute("""
            UPDATE Operation SET
                operation_type = COALESCE(?, operation_type),
                description    = COALESCE(?, description),
                made_by        = COALESCE(?, made_by),
                reviewed_by    = COALESCE(?, reviewed_by),
                material_cost  = COALESCE(?, material_cost),
                comments       = COALESCE(?, comments)
            WHERE id = ?
        """, (
            body.get("type"),
            body.get("description"),
            body.get("done_by"),
            body.get("validated_by"),
            body.get("material_cost"),
            body.get("comments"),
            operation_id
        ))

    return jsonify({"message": "Operation updated"}), 200