import os
from backend.utils.hair_analysis import analyze_hair

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "uploads", "sample_hair.jpg")

def test_hair():
    print("🔍 Testing Hair Image:", IMAGE_PATH)

    if not os.path.exists(IMAGE_PATH):
        print("❌ Image not found")
        return

    result = analyze_hair(IMAGE_PATH)

    print("\n🧠 HAIR ANALYSIS:")
    print("👉 Hair Type :", result["hair_type"])
    print("👉 Frizz     :", result["frizz"])
    print("👉 Damage    :", result["damage"])
    print("👉 Dandruff  :", result["dandruff"])

if __name__ == "__main__":
    test_hair()