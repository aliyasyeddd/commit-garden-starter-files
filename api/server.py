from flask import Flask, jsonify, send_from_directory
import json
import os
from datetime import date

# APP & PATHS
BASE_DIR    = os.path.dirname(__file__)
WEB_DIR     = os.path.join(BASE_DIR, '..', 'web')
DATA_DIR    = os.path.join(BASE_DIR, '..', 'data')
GARDEN_FILE = os.path.join(DATA_DIR, 'garden.json')

app = Flask(__name__, static_folder=WEB_DIR)

# STATIC FILES
@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")

@app.route("/styles.css")
def styles():
    return send_from_directory(WEB_DIR, "styles.css", mimetype="text/css")

@app.route("/app.js")
def scripts():
    return send_from_directory(WEB_DIR, "app.js", mimetype="application/javascript")

@app.route("/helpers.js")
def helpers():
    return send_from_directory(WEB_DIR, "helpers.js", mimetype="application/javascript")

@app.route("/constants.js")
def constants():
    return send_from_directory(WEB_DIR, "constants.js", mimetype="application/javascript")

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(WEB_DIR, "favicon.ico", mimetype="image/x-icon")


# GARDEN DATA (read-only for now)
@app.route("/garden-data")
def garden_data():
    with open(GARDEN_FILE, "r") as f:
        data = json.load(f)
    data["best_streak"] = max(data.get("best_streak", 0), data.get("streak", 0))
    return jsonify(data)

@app.route("/svg")
def svg():
    return send_from_directory(DATA_DIR, "garden.svg", mimetype="image/svg+xml")

@app.route("/logs")
def logs():
    return jsonify([])  # empty for now — logs come alive after commit is wired up


# START
if __name__ == "__main__":
    app.run(port=8000, debug=True)