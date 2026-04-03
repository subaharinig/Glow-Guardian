import os
import cv2
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib

from backend.utils.face_features import extract_features

DATASET_PATH = "dataset/train"
VALID_PATH = "dataset/valid"

label_map = {
    "acne": 0,
    "pimple": 1,
    "spots": 2
}

# LOAD DATA
def load_data(path):
    X, y = [], []

    for label in label_map:
        folder = os.path.join(path, label)

        for file in os.listdir(folder):
            img_path = os.path.join(folder, file)

            try:
                img = cv2.imread(img_path)
                features = extract_features(img)

                X.append(features)
                y.append(label_map[label])
            except:
                continue

    return np.array(X), np.array(y)

# Train data
X_train, y_train = load_data(DATASET_PATH)

# Validation data
X_val, y_val = load_data(VALID_PATH)

# MODEL
model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1
)

model.fit(X_train, y_train)

# VALIDATION
preds = model.predict(X_val)
acc = accuracy_score(y_val, preds)

print("Validation Accuracy:", acc)

# SAVE MODEL

MODEL_PATH = os.path.join("models", "skin_model.pkl")
joblib.dump(model, MODEL_PATH)
print("✅ Model saved")