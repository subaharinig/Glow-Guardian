from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from auth import auth
import os

# ======================================
# APP CONFIGURATION
# ======================================

# Path to frontend folder
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER,
    static_url_path=""
)

CORS(app)

# Upload folder (for AI image analysis later)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ======================================
# REGISTER BLUEPRINTS
# ======================================

app.register_blueprint(auth, url_prefix="/api/auth")


# ======================================
# SERVE FRONTEND PAGES
# ======================================

# Home Page
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


# Serve all static files (html, css, js, images)
@app.route("/<path:path>")
def serve_files(path):
    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return jsonify({"error": "File not found"}), 404


# ======================================
# IMAGE UPLOAD API (Future AI Analysis)
# ======================================

@app.route("/api/upload", methods=["POST"])
def upload_image():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(save_path)

    return jsonify({
        "message": "Image uploaded successfully",
        "file_path": save_path
    })


# ======================================
# HEALTH CHECK API
# ======================================

@app.route("/api/status")
def status():
    return jsonify({
        "status": "Glow Guardians API Running 🚀"
    })


# ======================================
# RUN SERVER
# ======================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
