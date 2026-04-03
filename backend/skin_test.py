import os
import cv2
import joblib

from utils.skin_features import extract_features, detect_skin_type



# ==============================
# PATHS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_model.pkl")
IMAGE_PATH = os.path.join(BASE_DIR, "uploads", "sample_3.jpg")  # 👈 change image name if needed

# ==============================
# LOAD MODEL
# ==============================
model = joblib.load(MODEL_PATH)

# Label mapping (reverse)
label_map = {
    0: "Allergy",
    1: "Infection",
    2: "Normal",
    3: "Rash"
}

# ==============================
# TEST FUNCTION
# ==============================
def test_image():
    print("🔍 Testing Image:", IMAGE_PATH)

    # Check image exists
    if not os.path.exists(IMAGE_PATH):
        print("❌ Image not found")
        return

    # Read image
    img = cv2.imread(IMAGE_PATH)

    if img is None:
        print("❌ Failed to load image")
        return

    # Extract features
    features = extract_features(img)

    # Predict
    pred = model.predict([features])[0]
    probs = model.predict_proba([features])[0]

    confidence = max(probs)
    features = extract_features(img)
    
    skin_type = detect_skin_type(features)



    

    # ==============================
    # OUTPUT
    # ==============================
    print("\n🧠 SKIN DISEASE ANALYSIS:")
    print("👉 Condition  :", label_map[pred])
    print("👉 Confidence :", round(confidence * 100, 2), "%")
    print("👉 Skin Type  :", skin_type)
    

    print("\n💡 Suggestions:")

    if pred == 0:  # Allergy
        print("✔ Avoid allergens")
        print("✔ Use anti-allergic cream")

    elif pred == 1:  # Infection
        print("✔ Keep area clean")
        print("✔ Consult doctor if severe")

    elif pred == 2:  # Normal
        print("✔ Maintain hygiene")
        print("✔ Use moisturizer")

    elif pred == 3:  # Rash
        print("✔ Use soothing lotion")
        print("✔ Avoid heat exposure")

    print("\n✅ TEST COMPLETED 🚀")


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    test_image()