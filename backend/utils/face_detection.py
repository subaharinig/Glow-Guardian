import cv2

def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(
        "backend/haarcascade/haarcascade_frontalface_default.xml"
    )

    img = cv2.imread(image_path)

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]

    return face