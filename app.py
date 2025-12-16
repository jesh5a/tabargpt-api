import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Allow ONLY your frontend site to call this API
CORS(app, resources={
    r"/*": {"origins": ["https://tabargpt.com", "https://www.tabargpt.com"]}
})

API_TOKEN = os.environ.get("API_TOKEN", "")

def require_token():
    # Simple token check (prevents random public abuse)
    if not API_TOKEN:
        return None  # if you forgot to set it, don't block you during testing
    provided = request.headers.get("X-API-KEY", "")
    if provided != API_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    return None

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/hello")
def hello():
    maybe = require_token()
    if maybe:
        return maybe
    return jsonify(message="Hello from api.tabargpt.com")
