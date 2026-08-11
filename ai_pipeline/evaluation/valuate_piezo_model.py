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

MODEL_FILE = r"ai_pipeline\models\piezo_random_forest.pkl"

TEST_FOLDER = r"ai_pipeline\training\dataset_split"

# ==========================================
# LOAD MODEL
# ==========================================

print("Loading trained model...")

model = joblib.load(MODEL_FILE)

# ==========================================
# LOAD TEST DATA
# ==========================================

print("Loading test dataset...")

X_test = pd.read_csv(
    os.path.join(TEST_FOLDER, "X_test.csv")
)

y_test = pd.read_csv(
    os.path.join(TEST_FOLDER, "y_test.csv")
).squeeze()

print("Test samples:", len(X_test))

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

print("\n================================")
print("MODEL EVALUATION")
print("================================")

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)

# ==========================================
# CLASSIFICATION REPORT
# ==========================================

class_names = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        labels=[0, 1, 2, 3],
        target_names=class_names,
        zero_division=0
    )
)

# ==========================================
# CONFUSION MATRIX
# ==========================================

print("Confusion Matrix:")

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1, 2, 3]
)

print(cm)

# ==========================================
# SAVE RESULTS
# ==========================================

OUTPUT_FILE = r"ai_pipeline\evaluation\piezo_evaluation.txt"

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

with open(OUTPUT_FILE, "w") as file:

    file.write("PIEZO MODEL EVALUATION\n")
    file.write("======================\n\n")

    file.write(
        f"Test Accuracy: {accuracy * 100:.2f}%\n\n"
    )

    file.write("Classification Report:\n")

    file.write(
        classification_report(
            y_test,
            y_pred,
            labels=[0, 1, 2, 3],
            target_names=class_names,
            zero_division=0
        )
    )

    file.write("\nConfusion Matrix:\n")
    file.write(str(cm))

print("\nEvaluation saved to:")
print(OUTPUT_FILE)
