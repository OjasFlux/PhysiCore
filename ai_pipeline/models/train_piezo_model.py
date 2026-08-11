import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ==========================================
# PATHS
# ==========================================

TRAIN_FOLDER = r"ai_pipeline\training\dataset_split"

MODEL_FOLDER = r"ai_pipeline\models"

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "piezo_random_forest.pkl"
)

# ==========================================
# LOAD TRAINING DATA
# ==========================================

print("Loading training dataset...")

X_train = pd.read_csv(
    os.path.join(TRAIN_FOLDER, "X_train.csv")
)

y_train = pd.read_csv(
    os.path.join(TRAIN_FOLDER, "y_train.csv")
).squeeze()

print("Training samples:", len(X_train))
print("Features:", X_train.shape[1])

# ==========================================
# LOAD VALIDATION DATA
# ==========================================

X_val = pd.read_csv(
    os.path.join(TRAIN_FOLDER, "X_validation.csv")
)

y_val = pd.read_csv(
    os.path.join(TRAIN_FOLDER, "y_validation.csv")
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

print("Training model...\n")

model.fit(
    X_train,
    y_train
)

print("Training completed.")

# ==========================================
# VALIDATION
# ==========================================

y_pred = model.predict(X_val)

accuracy = accuracy_score(
    y_val,
    y_pred
)

print("\n================================")
print("VALIDATION RESULT")
print("================================")

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
