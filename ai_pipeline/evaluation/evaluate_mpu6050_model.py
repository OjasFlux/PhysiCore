import pandas as pd
import joblib
import os

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# PATHS
# ==========================================

MODEL_FILE = r"ai_pipeline\models\mpu6050_random_forest.pkl"

TEST_FOLDER = r"ai_pipeline\training\mpu6050_dataset_split"

OUTPUT_FILE = (
    r"ai_pipeline\evaluation"
    r"\mpu6050_evaluation.txt"
)

# ==========================================
# LOAD MODEL
# ==========================================

print("Loading MPU6050 model...")

model = joblib.load(MODEL_FILE)

# ==========================================
# LOAD TEST DATA
# ==========================================

print("Loading MPU6050 test dataset...")

X_test = pd.read_csv(
    os.path.join(
        TEST_FOLDER,
        "X_test.csv"
    )
)

y_test = pd.read_csv(
    os.path.join(
        TEST_FOLDER,
        "y_test.csv"
    )
).squeeze()

print("Test samples:", len(X_test))
print("Features:", X_test.shape[1])

# ==========================================
# PREDICTION
# ==========================================

print("\nRunning predictions...")

y_pred = model.predict(X_test)

# ==========================================
# ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

# ==========================================
# CLASSIFICATION REPORT
# ==========================================

class_names = [
    "Normal",
    "Minor Fault",
    "Moderate Fault",
    "Severe Fault"
]

report = classification_report(
    y_test,
    y_pred,
    labels=[0, 1, 2, 3],
    target_names=class_names,
    zero_division=0
)

# ==========================================
# CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1, 2, 3]
)

# ==========================================
# PRINT RESULTS
# ==========================================

print("\n======================================")
print("MPU6050 MODEL EVALUATION")
print("======================================")

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")
print(report)

print("Confusion Matrix:")
print(cm)

# ==========================================
# SAVE REPORT
# ==========================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "PHYSICORE MPU6050 MODEL EVALUATION\n"
    )

    file.write(
        "==================================\n\n"
    )

    file.write(
        f"Test Samples: {len(X_test)}\n"
    )

    file.write(
        f"Test Accuracy: {accuracy * 100:.2f}%\n\n"
    )

    file.write(
        "Classification Report:\n\n"
    )

    file.write(report)

    file.write(
        "\nConfusion Matrix:\n"
    )

    file.write(str(cm))

print("\nEvaluation report saved to:")
print(OUTPUT_FILE)
