# routes_debug.py
from flask import Blueprint, request, jsonify
debug_bp = Blueprint("debug", __name__)

@debug_bp.route("/debug-ip")
def debug_ip():
    return jsonify({
        "remote_addr": request.remote_addr,
        "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        "X-Real-IP": request.headers.get("X-Real-IP"),
    })
