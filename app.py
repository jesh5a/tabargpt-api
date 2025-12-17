from flask import Flask, request, jsonify
import time

# ================= FLASK APP =================
app = Flask(__name__)

# ================= STORAGE =================
visit_logs = []

# ================= HELPERS =================
def get_client_ip(req):
    # 1) Cloudflare real visitor IP
    cf_ip = req.headers.get("CF-Connecting-IP")
    if cf_ip:
        return cf_ip.strip()

    # 2) Proxy chain
    xff = req.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()

    # 3) Fallback
    return req.remote_addr

# ================= ROUTES =================
@app.route("/api/visit", methods=["GET", "POST"])
def api_visit():
    ip = get_client_ip(request)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "ip": ip,
        "time": timestamp,
        "ua": request.headers.get("User-Agent", ""),
        "ref": request.headers.get("Referer", ""),
    }

    visit_logs.append(entry)

    print(
        f"[VISIT] IP={ip} TIME={timestamp} "
        f"UA={entry['ua']} REF={entry['ref']}",
        flush=True
    )

    return jsonify({"status": "ok"}), 200
