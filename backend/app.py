from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# IMPORTANT: remove "backend." if running inside backend folder
from backend.routes.auth_routes import auth

from backend.utils.face_detection import detect_face
from backend.utils.skin_analysis import full_analysis
from backend.utils.hair_analysis import analyze_hair
from backend.utils.disease_analysis import analyze_disease
from backend.utils.recommendation import get_recommendation

import os

# ======================================
# APP CONFIGURATION
# ======================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Frontend path
FRONTEND_FOLDER = os.path.join(BASE_DIR, "../frontend")

app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER,
    static_url_path=""
)

CORS(app)

# Upload config
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB limit

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


# ======================================
# HELPER FUNCTIONS
# ======================================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)
    return save_path


# ======================================
# REGISTER BLUEPRINTS
# ======================================

app.register_blueprint(auth, url_prefix="/api/auth")


# ======================================
# SERVE FRONTEND
# ======================================

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "landing.html")


@app.route("/<path:path>")
def serve_files(path):
    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return jsonify({"error": "File not found"}), 404


# ======================================
# SKIN ANALYSIS API (UPDATED)
# ======================================

@app.route("/api/skin-analysis", methods=["POST"])
def skin_analysis():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "Invalid file type"}), 400

        save_path = save_file(image)

        # Face Detection
        face = detect_face(save_path)

        if face is None:
            return jsonify({"error": "No face detected"}), 400

        # ✅ FULL AI ANALYSIS
        result = full_analysis(face)

        # Recommendation
        recommendation = get_recommendation(result["skin_type"])

        return jsonify({
            "success": True,
            **result,
            "recommendation": recommendation
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ======================================
# HAIR ANALYSIS API
# ======================================

@app.route("/api/hair-analysis", methods=["POST"])
def hair_analysis():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "Invalid file type"}), 400

        save_path = save_file(image)

        result = analyze_hair(save_path)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ======================================
# DISEASE ANALYSIS API
# ======================================

@app.route("/api/disease-analysis", methods=["POST"])
def disease_analysis():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(image.filename):
            return jsonify({"error": "Invalid file type"}), 400

        save_path = save_file(image)

        result = analyze_disease(save_path)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ======================================
# HEALTH CHECK API
# ======================================

@app.route("/api/status")
def status():
    return jsonify({
        "success": True,
        "message": "Glow Guardians API Running 🚀"
    })


# ======================================
# GLOBAL ERROR HANDLER
# ======================================

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File too large (Max 5MB)"}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404


# ======================================
# RUN SERVER
# ======================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)