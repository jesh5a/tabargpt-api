from flask import Flask, request, jsonify
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

@app.route("/api/visit", methods=["GET", "POST"])
def visit():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        page = data.get("page")
        ref = data.get("ref")
    else:  # GET
        page = request.args.get("page")
        ref = request.args.get("ref")

    ip = (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0]
        or request.remote_addr
    )
    
    ua = request.headers.get("User-Agent")
    
    log = {
        "time": datetime.utcnow().isoformat(),
        "method": request.method,
        "ip": ip,
        "page": page,
        "ref": ref,
        "ua": ua
    }
    
    print("[VISIT]", log)
    
    return jsonify({"status": "ok"})
