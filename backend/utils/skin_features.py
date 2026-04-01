import cv2
import numpy as np

def extract_features(face):

    face = cv2.resize(face, (224, 224))
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

    # 🔴 Redness (pimples)
    red = face[:, :, 2]
    green = face[:, :, 1]
    redness = np.mean(red - green)

    # 🌟 Brightness (skin type / tan)
    brightness = np.mean(gray)

    # 🧵 Texture (dry skin)
    texture = np.var(gray)

    # 🔳 Wrinkles (edges)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.mean(edges)

    # 🟤 Dark spots (color variation)
    color_var = np.var(face)

    return [redness, brightness, texture, edge_density, color_var]