import os
import cv2
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import warnings
warnings.filterwarnings("ignore")

from utils.skin_features import extract_features

# ==============================
# PATHS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset_skin")

TRAIN_PATH = os.path.join(DATASET_PATH, "train")
VALID_PATH = os.path.join(DATASET_PATH, "valid")

# Label mapping
label_map = {
    "allergy": 0,
    "infection": 1,
    "normal": 2,
    "rash": 3
}

# ==============================
# LOAD DATA
# ==============================
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




# ==============================
# TRAIN
# ==============================
print("🚀 Loading data...")

X_train, y_train = load_data(TRAIN_PATH)
X_val, y_val = load_data(VALID_PATH)

print("✅ Data loaded")

model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1
)

model.fit(X_train, y_train)

# ==============================
# VALIDATION
# ==============================
preds = model.predict(X_val)
acc = accuracy_score(y_val, preds)

print("🎯 Validation Accuracy:", acc)

# ==============================
# SAVE MODEL
# ==============================
MODEL_PATH = os.path.join(BASE_DIR, "models", "disease_model.pkl")
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("✅ Model saved at:", MODEL_PATH)