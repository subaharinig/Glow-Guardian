import cv2
import numpy as np

# ==============================
# FEATURE EXTRACTION
# ==============================
def extract_features(image):
    """
    Extract features from image
    Returns: list of numerical features
    """

    if image is None:
        return None

    image = cv2.resize(image, (224, 224))

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 🔴 Redness (infection / rash)
    red = image[:, :, 2]
    green = image[:, :, 1]
    redness = np.mean(red - green)

    # 🌟 Brightness
    brightness = np.mean(gray)

    # 🧵 Texture (dry skin)
    texture = np.var(gray)

    # 🔳 Edge density (roughness)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges)

    # 🟤 Color variation (uneven skin)
    color_var = np.var(image)

    # 🎨 Saturation
    saturation = np.mean(hsv[:, :, 1])

    # 🌈 Hue variance
    hue_var = np.var(hsv[:, :, 0])

    return [
        redness,
        brightness,
        texture,
        edge_density,
        color_var,
        saturation,
        hue_var
    ]


# ==============================
# SKIN TYPE DETECTION
# ==============================
def detect_skin_type(features):
    """
    Detect skin type using extracted features
    """

    if features is None:
        return "Unknown"

    _, brightness, texture, _, _, _, _ = features

    if brightness > 150:
        return "Oily"
    elif texture > 500:
        return "Dry"
    else:
        return "Normal"