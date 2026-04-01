import os
import cv2

# ✅ Correct imports
from backend.utils.face_detection import detect_face
from backend.utils.skin_analysis import full_analysis
from backend.utils.recommendation import get_recommendation

# ===============================
# IMAGE PATH
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "uploads", "sample2.jpg")


def test_image():
    print("🔍 Testing Image:", IMAGE_PATH)

    # Check file exists
    if not os.path.exists(IMAGE_PATH):
        print("❌ Image not found")
        return

    # ===============================
    # STEP 1: FACE DETECTION
    # ===============================
    face = detect_face(IMAGE_PATH)

    if face is None:
        print("❌ No face detected")
        return

    print("✅ Face detected")

    # ===============================
    # STEP 2: FULL ANALYSIS
    # ===============================
    result = full_analysis(face)

    print("\n🧠 FULL SKIN ANALYSIS:")
    print("👉 Issue       :", result["issue"])
    print("👉 Skin Type   :", result["skin_type"])
    print("👉 Tan Level   :", result["tan"])
    print("👉 Wrinkles    :", result["wrinkles"])

    # ===============================
    # STEP 3: RECOMMENDATION
    # ===============================
    rec = get_recommendation(result["skin_type"])

    print("\n💡 Recommendations:")
    for r in rec:
        print("✔", r)

    print("\n✅ TEST COMPLETED SUCCESSFULLY 🚀")


# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    test_image()