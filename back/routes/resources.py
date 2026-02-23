from flask import Blueprint, Response, jsonify
from back.database import get_db

resources_bp = Blueprint("resources", __name__)

@resources_bp.get("/resources")
def list_resources() -> Response:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM resource").fetchall()
    
    return jsonify([dict(r) for r in rows])