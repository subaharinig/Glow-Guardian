import cv2
import numpy as np

def analyze_hair(path):

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    texture = np.var(gray)

    if texture > 500:
        frizz = "High"
    else:
        frizz = "Low"

    return {
        "frizz_level": frizz,
        "summary": f"Hair frizz level detected as {frizz}"
    }

      
