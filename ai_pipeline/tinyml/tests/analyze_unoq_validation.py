import pandas as pd
import os

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# ==========================================
# VALIDATION FILES
# ==========================================

INPUT_FILES = [
    r"ai_pipeline\tinyml\tests\normal_validation.csv",
    r"ai_pipeline\tinyml\tests\minor_validation.csv",
    r"ai_pipeline\tinyml\tests\moderate_validation.csv",
    r"ai_pipeline\tinyml\tests\severe_validation.csv"
]

CLASS_NAMES = [
    "Normal",
    "Minor Fault",
    "Moderate Fault",
    "Severe Fault"
]

# ==========================================
# LOAD FILES
# ==========================================

print("Loading UNO Q validation data...\n")

dataframes = []

for file in INPUT_FILES:

    if not os.path.exists(file):
        print("File not found:")
        print(file)
        continue

    df = pd.read_csv(file)

    dataframes.append(df)

    print(
        os.path.basename(file),
        "->",
        len(df),
        "windows"
    )

if len(dataframes) == 0:
    raise FileNotFoundError(
        "No validation files found."
    )

# ==========================================
# COMBINE DATA
# ==========================================

df = pd.concat(
    dataframes,
    ignore_index=True
)

# ==========================================
# VALIDATE REQUIRED COLUMNS
# ==========================================

required_columns = [
    "Prediction",
    "Expected"
]

for column in required_columns:

    if column not in df.columns:
        raise ValueError(
            f"Missing required column: {column}"
        )

# ==========================================
# CALCULATE RESULTS
# ==========================================

y_true = df["Expected"].astype(int)

y_pred = df["Prediction"].astype(int)

accuracy = accuracy_score(
    y_true,
    y_pred
)

correct = (y_true == y_pred).sum()

incorrect = len(df) - correct

# ==========================================
# PRINT SUMMARY
# ==========================================

print("\n======================================")
print("UNO Q HARDWARE VALIDATION")
print("======================================")

print("Total windows :", len(df))
print("Correct       :", correct)
print("Incorrect     :", incorrect)

print(
    f"Hardware Accuracy : {accuracy * 100:.2f}%"
)

# ==========================================
# CLASSIFICATION REPORT
# ==========================================

report = classification_report(
    y_true,
    y_pred,
    labels=[0, 1, 2, 3],
    target_names=CLASS_NAMES,
    zero_division=0
)

print("\nClassification Report:\n")
print(report)

# ==========================================
# CONFUSION MATRIX
# ==========================================

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1, 2, 3]
)

print("Confusion Matrix:")
print(cm)

# ==========================================
# CLASS-WISE ACCURACY
# ==========================================

print("\nClass-wise Accuracy:")

class_results = []

for class_id, class_name in enumerate(CLASS_NAMES):

    class_rows = df[
        df["Expected"] == class_id
    ]

    total_class_samples = len(class_rows)

    if total_class_samples == 0:

        class_accuracy = 0.0

        print(
            f"{class_name}: No data"
        )

    else:

        correct_class_samples = (
            class_rows["Prediction"] == class_id
        ).sum()

        class_accuracy = (
            correct_class_samples /
            total_class_samples
        ) * 100

        print(
            f"{class_name}: "
            f"{class_accuracy:.2f}% "
            f"({correct_class_samples}/"
            f"{total_class_samples})"
        )

    class_results.append(
        (
            class_name,
            class_accuracy,
            total_class_samples
        )
    )

# ==========================================
# SAVE REPORT
# ==========================================

OUTPUT_FILE = (
    r"ai_pipeline\tinyml\tests"
    r"\uno_q_hardware_validation.txt"
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "PHYSICORE UNO Q HARDWARE VALIDATION\n"
    )

    file.write(
        "====================================\n\n"
    )

    file.write(
        f"Total Windows: {len(df)}\n"
    )

    file.write(
        f"Correct Predictions: {correct}\n"
    )

    file.write(
        f"Incorrect Predictions: {incorrect}\n"
    )

    file.write(
        f"Hardware Accuracy: "
        f"{accuracy * 100:.2f}%\n\n"
    )

    file.write(
        "Classification Report:\n\n"
    )

    file.write(report)

    file.write(
        "\nConfusion Matrix:\n"
    )

    file.write(
        str(cm)
    )

    file.write(
        "\n\nClass-wise Accuracy:\n"
    )

    for name, acc, count in class_results:

        file.write(
            f"{name}: {acc:.2f}% "
            f"({count} windows)\n"
        )

print("\n======================================")
print("ANALYSIS COMPLETED")
print("======================================")

print("Report saved to:")
print(OUTPUT_FILE)