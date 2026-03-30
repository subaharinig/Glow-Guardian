import cv2
import numpy as np

def analyze_hair(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return {"error": "Invalid image"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    brightness = np.mean(gray)

    # Oil / Dry detection
    if brightness > 150:
        hair_type = "Oily Scalp"
    else:
        hair_type = "Dry Scalp"

    # Dandruff detection (white pixels)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    white_pixels = np.sum(thresh == 255)

    if white_pixels > 5000:
        issue = "Possible dandruff detected"
    else:
        issue = "No major dandruff"

    return {
        "hair_type": hair_type,
        "issue": issue,
        "recommendation": "Use mild shampoo and maintain scalp hygiene"
    }