from flask import Blueprint, jsonify
from back.database import get_db

resources_bp = Blueprint("resources", __name__)

@resources_bp.get("/resources")
def list_resources():
    conn = get_db()
    rows = conn.execute("SELECT * FROM resource").fetchall()
    conn.close()
    
    return jsonify([dict(r) for r in rows])