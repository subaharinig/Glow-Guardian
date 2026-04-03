import joblib
import os
import numpy as np

from backend.utils.face_features import extract_features
from backend.utils.recommendation import get_face_recommendation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "skin_model.pkl")

model = joblib.load(MODEL_PATH)

label_map = {
    0: "Acne",
    1: "Pimple",
    2: "Spots"
}


def analyze_skin(face):
    features = extract_features(face)

    pred = model.predict([features])[0]
    prob = model.predict_proba([features])[0]

    confidence = float(np.max(prob)) * 100

    return label_map[pred], round(confidence, 2)


def analyze_additional(face):

    features = extract_features(face)
    redness, brightness, texture, edges, color_var = features

    if brightness > 150:
        skin_type = "Oily"
    elif texture > 500:
        skin_type = "Dry"
    else:
        skin_type = "Normal"

    if brightness < 100:
        tan = "High"
    elif brightness < 140:
        tan = "Medium"
    else:
        tan = "Low"

    if edges > 25:
        wrinkles = "High"
    elif edges > 15:
        wrinkles = "Medium"
    else:
        wrinkles = "Low"

    return skin_type, tan, wrinkles


def full_analysis(face):

    issue, confidence = analyze_skin(face)
    skin_type, tan, wrinkles = analyze_additional(face)

    recommendation = get_face_recommendation(issue, skin_type)

    return {
        "success": True,
        "issue": issue,   # ✅ FIXED
        "confidence": confidence,
        "skin_type": skin_type,
        "tan": tan,
        "wrinkles": wrinkles,
        "recommendation": recommendation,
        "summary": f"You have {issue} with {skin_type} skin. "
                   f"Tan level is {tan} and wrinkles are {wrinkles}."
    }