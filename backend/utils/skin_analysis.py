import numpy as np

def analyze_skin(face):

    brightness = np.mean(face)
    contrast = np.std(face)

    # Skin Type
    if brightness < 80:
        skin_type = "Dry"
    elif brightness > 160:
        skin_type = "Oily"
    else:
        skin_type = "Normal"

    # Acne Detection (simple texture logic)
    if contrast > 50:
        acne = "Possible acne detected"
    else:
        acne = "No major acne"

    return skin_type, acne