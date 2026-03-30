from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from backend.routes.auth_routes import auth

# Import AI utils
from backend.utils.face_detection import detect_face
from backend.utils.skin_analysis import analyze_skin
from backend.utils.hair_analysis import analyze_hair
from backend.utils.disease_analysis import analyze_disease
from backend.utils.recommendation import get_recommendation

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

# Upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ======================================
# REGISTER BLUEPRINTS
# ======================================

app.register_blueprint(auth, url_prefix="/api/auth")


# ======================================
# SERVE FRONTEND
# ======================================

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_files(path):
    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return jsonify({"error": "File not found"}), 404


# ======================================
# SKIN ANALYSIS API
# ======================================

@app.route("/api/skin-analysis", methods=["POST"])
def skin_analysis():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(save_path)

    # Face Detection
    face = detect_face(save_path)

    if face is None:
        return jsonify({"error": "No face detected"}), 400

    # Skin Analysis
    skin_type, acne = analyze_skin(face)

    # Recommendation
    recommendation = get_recommendation(skin_type)

    return jsonify({
        "skin_type": skin_type,
        "acne": acne,
        "recommendation": recommendation
    })


# ======================================
# HAIR ANALYSIS API
# ======================================

@app.route("/api/hair-analysis", methods=["POST"])
def hair_analysis():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(save_path)

    result = analyze_hair(save_path)

    return jsonify(result)


# ======================================
# DISEASE ANALYSIS API
# ======================================

@app.route("/api/disease-analysis", methods=["POST"])
def disease_analysis():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(save_path)

    result = analyze_disease(save_path)

    return jsonify(result)


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