import cv2
import numpy as np

def analyze_disease(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return {"error": "Invalid image"}

    # Extract red channel
    red_channel = img[:, :, 2]

    avg_red = np.mean(red_channel)

    # Simple redness detection
    if avg_red > 150:
        condition = "Possible skin irritation or rash"
    else:
        condition = "Skin appears normal"

    return {
        "condition": condition,
        "recommendation": "Use soothing skincare products and consult if severe"
    }