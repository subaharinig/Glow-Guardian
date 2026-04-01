import joblib
import os
import numpy as np

from backend.utils.skin_features import extract_features

# ======================================
# LOAD MODEL
# ======================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "skin_model.pkl")

model = joblib.load(MODEL_PATH)

# ======================================
# LABEL MAP
# ======================================

label_map = {
    0: "Acne",
    1: "Pimple",
    2: "Spots"
}

# ======================================
# MAIN ISSUE PREDICTION (ML MODEL)
# ======================================

def analyze_skin(face):
    """
    Predict main skin issue using trained XGBoost model
    """

    features = extract_features(face)
    pred = model.predict([features])[0]

    # Confidence score (optional but powerful 🔥)
    prob = model.predict_proba([features])[0]
    confidence = float(np.max(prob))

    return label_map[pred], confidence


# ======================================
# ADDITIONAL ANALYSIS (RULE-BASED)
# ======================================

def analyze_additional(face):
    """
    Detect:
    - Skin Type
    - Tan Level
    - Wrinkles
    """

    features = extract_features(face)
    redness, brightness, texture, edges, color_var = features

    # -------------------------
    # Skin Type Detection
    # -------------------------
    if brightness > 150:
        skin_type = "Oily"
    elif texture > 500:
        skin_type = "Dry"
    else:
        skin_type = "Normal"

    # -------------------------
    # Tan Detection
    # -------------------------
    if brightness < 100:
        tan = "High"
    elif brightness < 140:
        tan = "Medium"
    else:
        tan = "Low"

    # -------------------------
    # Wrinkle Detection
    # -------------------------
    if edges > 25:
        wrinkles = "High"
    elif edges > 15:
        wrinkles = "Medium"
    else:
        wrinkles = "Low"

    return skin_type, tan, wrinkles


# ======================================
# FULL ANALYSIS (FINAL OUTPUT)
# ======================================

def full_analysis(face):
    """
    Complete pipeline:
    - ML prediction
    - Additional features
    - Summary generation
    """

    issue, confidence = analyze_skin(face)
    skin_type, tan, wrinkles = analyze_additional(face)

    return {
        "issue": issue,
        "confidence": round(confidence, 2),
        "skin_type": skin_type,
        "tan": tan,
        "wrinkles": wrinkles,
        "summary": f"You have {issue} with {skin_type} skin. "
                   f"Tan level is {tan} and wrinkles are {wrinkles}."
    }