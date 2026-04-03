import cv2
import numpy as np

from backend.utils.recommendation import get_hair_recommendation

def analyze_hair(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return {"error": "Image not found"}

    img = cv2.resize(img, (224, 224))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 🌟 Brightness (Hair Type)
    brightness = np.mean(gray)

    if brightness > 150:
        hair_type = "Oily"
    elif brightness < 90:
        hair_type = "Dry"
    else:
        hair_type = "Normal"

    # 🧵 Texture (Frizz)
    texture = np.var(gray)

    if texture > 500:
        frizz = "High"
    elif texture > 200:
        frizz = "Medium"
    else:
        frizz = "Low"

    # 🔳 Damage (Edges)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges)

    if edge_density > 25:
        damage = "High"
    elif edge_density > 10:
        damage = "Medium"
    else:
        damage = "Low"

    # ❄️ Dandruff (White pixels detection)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    white_ratio = np.sum(mask) / (224 * 224)

    if white_ratio > 0.15:
        dandruff = "High"
    elif white_ratio > 0.05:
        dandruff = "Medium"
    else:
        dandruff = "Low"


    recommendation = get_hair_recommendation(hair_type, frizz, damage, dandruff)

    return {
    "hair_type": hair_type,
    "frizz": frizz,
    "damage": damage,
    "dandruff": dandruff,
    "recommendation": recommendation   # ✅ ADD
}
