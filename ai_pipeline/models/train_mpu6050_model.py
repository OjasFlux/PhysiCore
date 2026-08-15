import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ==========================================
# PATHS
# ==========================================

DATASET_FOLDER = r"ai_pipeline\training\mpu6050_dataset_split"

MODEL_FOLDER = r"ai_pipeline\models"

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "mpu6050_random_forest.pkl"
)


# ==========================================
# LOAD TRAINING DATA
# ==========================================

print("Loading MPU6050 training data...")

X_train = pd.read_csv(
    os.path.join(
        DATASET_FOLDER,
        "X_train.csv"
    )
)

y_train = pd.read_csv(
    os.path.join(
        DATASET_FOLDER,
        "y_train.csv"
    )
).squeeze()

print("Training samples:", len(X_train))
print("Features:", X_train.shape[1])


# ==========================================
# LOAD VALIDATION DATA
# ==========================================

X_val = pd.read_csv(
    os.path.join(
        DATASET_FOLDER,
        "X_validation.csv"
    )
)

y_val = pd.read_csv(
    os.path.join(
        DATASET_FOLDER,
        "y_validation.csv"
    )
).squeeze()

print("Validation samples:", len(X_val))


# ==========================================
# CREATE MODEL
# ==========================================

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# ==========================================
# TRAIN
# ==========================================

print("Training model...")

model.fit(
    X_train,
    y_train
)

print("Training completed.")


# ==========================================
# VALIDATION
# ==========================================

y_pred = model.predict(
    X_val
)

accuracy = accuracy_score(
    y_val,
    y_pred
)


# ==========================================
# RESULT
# ==========================================

print("\n======================================")
print("MPU6050 MODEL VALIDATION")
print("======================================")

print(
    f"Validation Accuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

print("\nModel saved to:")
print(MODEL_FILE)
