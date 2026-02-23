from flask import Flask, Response, send_from_directory
from flask_cors import CORS

# Routes
from back.routes.drones import drones_bp

# App parameters
HOST = "0.0.0.0"
PORT = 5000

# Flask app
app = Flask(__name__, static_folder="front/static")
app.register_blueprint(drones_bp)
CORS(app)

# Serve index.html by default
@app.route("/")
def index():
    return send_from_directory("front", "index.html")

# Tells the browser that OctoFlow doesn't have a favicon.ico
@app.route("/favicon.ico")
def favicon():
    return Response(status=204)

if __name__ == "__main__":	
	app.run(host=HOST, port=PORT, debug=True)
