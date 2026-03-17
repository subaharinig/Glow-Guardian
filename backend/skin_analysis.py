import cv2
import numpy as np

def analyze_skin(path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    brightness = np.mean(gray)

    if brightness < 80:
        skin_type = "Dry"
    else:
        skin_type = "Oily"

    return {
        "skin_type": skin_type,
        "skin_score": int(brightness % 100),
        "summary": f"Skin appears {skin_type}. Moisturizing recommended."
    }
