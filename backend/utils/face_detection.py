import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection

def detect_face(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_face.FaceDetection(min_detection_confidence=0.5) as face_detection:
        results = face_detection.process(img_rgb)

        if not results.detections:
            return None

        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box

            h, w, _ = img.shape
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            w_box = int(bbox.width * w)
            h_box = int(bbox.height * h)

            face = img[y:y+h_box, x:x+w_box]
            return face

    return None