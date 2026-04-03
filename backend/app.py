from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from backend.routes.auth_routes import auth

# AI Modules
from backend.utils.face_detection import detect_face
from backend.utils.face_analysis import full_analysis as face_analysis
from backend.utils.hair_analysis import analyze_hair
from backend.utils.skin_features import extract_features, detect_skin_type

import os
import cv2
import joblib

# ======================================
# APP CONFIG
# ======================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR, "../frontend")

app = Flask(__name__, static_folder=FRONTEND_FOLDER, static_url_path="")
CORS(app)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# ======================================
# LOAD MODELS (ONLY ONCE 🔥)
# ======================================

MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_model.pkl")
disease_model = joblib.load(MODEL_PATH)

label_map = {
    0: "Allergy",
    1: "Infection",
    2: "Normal",
    3: "Rash"
}

# ======================================
# HELPERS
# ======================================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    return path


# ======================================
# AUTH
# ======================================

app.register_blueprint(auth, url_prefix="/api/auth")


# ======================================
# FRONTEND
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
# 1️⃣ FACE ANALYSIS
# ======================================

@app.route("/api/face-analysis", methods=["POST"])
def analyze_face():
    try:
        image = request.files.get("image")

        if not image or image.filename == "":
            return jsonify({"error": "No image uploaded"}), 400

        save_path = save_file(image)

        face = detect_face(save_path)

        if face is None:
            return jsonify({"error": "No face detected"}), 400

        result = face_analysis(face)

        return jsonify({
            "success": True,
            **result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================
# 2️⃣ HAIR ANALYSIS
# ======================================

@app.route("/api/hair-analysis", methods=["POST"])
def analyze_hair_api():
    try:
        image = request.files.get("image")

        if not image or image.filename == "":
            return jsonify({"error": "No image uploaded"}), 400

        save_path = save_file(image)

        result = analyze_hair(save_path)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# ======================================
# 3️⃣ SKIN ANALYSIS (FINAL ✅)
# ======================================

@app.route("/api/skin-analysis", methods=["POST"])
def analyze_skin():
    try:
        image = request.files.get("image")

        if not image or image.filename == "":
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        save_path = save_file(image)

        img = cv2.imread(save_path)

        if img is None:
            return jsonify({"success": False, "error": "Failed to read image"}), 400

        # Extract Features
        features = extract_features(img)

        # Predict Disease
        pred = disease_model.predict([features])[0]
        probs = disease_model.predict_proba([features])[0]

        confidence = float(max(probs))
        condition = label_map[pred]

        # Detect Skin Type
        skin_type = detect_skin_type(features)

        # Recommendations
        if pred == 0:
            rec = ["Avoid allergens", "Use anti-allergic cream"]
        elif pred == 1:
            rec = ["Keep area clean", "Consult doctor if severe"]
        elif pred == 2:
            rec = ["Maintain hygiene", "Use moisturizer"]
        else:
            rec = ["Use soothing lotion", "Avoid heat exposure"]

        return jsonify({
            "success": True,
            "condition": condition,
            "confidence": round(confidence * 100, 2),
            "skin_type": skin_type,
            "recommendation": rec
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ======================================
# STATUS
# ======================================

@app.route("/api/status")
def status():
    return jsonify({
        "success": True,
        "message": "Glow Guardians API Running 🚀"
    })


# ======================================
# ERRORS
# ======================================

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File too large"}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404


# ======================================
# RUN
# ======================================

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)