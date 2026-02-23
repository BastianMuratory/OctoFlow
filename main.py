from __future__ import annotations

import inspect
import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
DB_PATH = Path("resources.db")

@app.route("/")
def index():
    return send_from_directory("front", "index.html")

if __name__ == "__main__":	
	app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
