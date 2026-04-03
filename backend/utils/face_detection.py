import cv2
import os

# Path to haarcascade file
cascade_path = os.path.join(
    os.path.dirname(__file__),
    "../haarcascade/haarcascade_frontalface_default.xml"
)

face_cascade = cv2.CascadeClassifier(cascade_path)


def detect_face(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    if len(faces) == 0:
        return None

    # Take first detected face
    x, y, w, h = faces[0]

    face = img[y:y+h, x:x+w]

    return face