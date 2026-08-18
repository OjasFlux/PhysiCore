import os
import glob
import pickle

import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from ai_pipeline.feature_engineering.mpu6050_features import (
    mpu6050_features
)


# =====================================================
# SETTINGS
# =====================================================

DATASET_ROOT = r"dataset\Processed_dataset\MPU6050"

MODEL_DIR = r"ai_pipeline\models"

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "mpu6050_decision_tree.pkl"
)

TEST_SIZE = 0.20

RANDOM_STATE = 42


# =====================================================
# CLASS MAP
# =====================================================

CLASS_MAP = {
    "Normal": 0,
    "Minor_Fault": 1,
    "Moderate_Fault": 2,
    "Severe_Fault": 3
}

CLASS_NAMES = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]


# =====================================================
# CREATE MODEL DIRECTORY
# =====================================================

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# =====================================================
# START
# =====================================================

print()
print("==============================================")
print("PHYSICORE MPU6050 TRAINING PIPELINE")
print("==============================================")
print()

print(
    "Dataset:",
    DATASET_ROOT
)

print()


# =====================================================
# LOAD WINDOWS
# =====================================================

X = []
y = []

total_files = 0


for class_name, class_id in CLASS_MAP.items():

    folder = os.path.join(
        DATASET_ROOT,
        class_name
    )

    if not os.path.isdir(folder):

        raise FileNotFoundError(
            "Class folder not found:\n"
            + folder
        )


    files = sorted(
        glob.glob(
            os.path.join(
                folder,
                "*.csv"
            )
        )
    )


    print(
        f"{class_name:<18}: "
        f"{len(files)} windows"
    )


    for file_path in files:

        df = pd.read_csv(
            file_path
        )


        features = extract_mpu6050_features(
            df
        )


        if len(features) != 56:

            raise RuntimeError(
                "Feature extraction returned "
                f"{len(features)} features."
            )


        X.append(
            features
        )

        y.append(
            class_id
        )

        total_files += 1


# =====================================================
# NUMPY
# =====================================================

X = np.asarray(
    X,
    dtype=np.float64
)

y = np.asarray(
    y,
    dtype=np.int32
)


print()
print(
    "Total windows:",
    total_files
)

print(
    "Feature count:",
    X.shape[1]
)


# =====================================================
# TRAIN / TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)


print()
print(
    "Training windows:",
    len(X_train)
)

print(
    "Testing windows:",
    len(X_test)
)


# =====================================================
# DECISION TREE
# =====================================================

print()
print(
    "Training Decision Tree..."
)


model = DecisionTreeClassifier(
    max_depth=8,
    min_samples_leaf=2,
    random_state=RANDOM_STATE
)


model.fit(
    X_train,
    y_train
)


# =====================================================
# PREDICTION
# =====================================================

y_pred = model.predict(
    X_test
)


# =====================================================
# ACCURACY
# =====================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print()
print("==============================================")
print("MODEL RESULT")
print("==============================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# =====================================================
# CLASSIFICATION REPORT
# =====================================================

print()
print("CLASSIFICATION REPORT")
print("----------------------------------------------")

report = classification_report(
    y_test,
    y_pred,
    labels=[0, 1, 2, 3],
    target_names=CLASS_NAMES,
    digits=4,
    zero_division=0
)

print(
    report
)


# =====================================================
# CONFUSION MATRIX
# =====================================================

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=[0, 1, 2, 3]
)

print()
print("CONFUSION MATRIX")
print("----------------------------------------------")
print(
    "Rows = Actual"
)
print(
    "Columns = Predicted"
)
print()
print(cm)


# =====================================================
# TREE INFORMATION
# =====================================================

print()
print("TREE INFORMATION")
print("----------------------------------------------")

print(
    "Depth:",
    model.get_depth()
)

print(
    "Nodes:",
    model.tree_.node_count
)


# =====================================================
# FEATURE IMPORTANCE
# =====================================================

print()
print("TOP FEATURE IMPORTANCE")
print("----------------------------------------------")


SIGNALS = [
    "Ax",
    "Ay",
    "Az",
    "Gx",
    "Gy",
    "Gz",
    "AccelMag",
    "GyroMag"
]

STATISTICS = [
    "Mean",
    "Std",
    "Variance",
    "RMS",
    "Maximum",
    "Minimum",
    "Peak_to_Peak"
]


feature_names = []

for signal in SIGNALS:

    for statistic in STATISTICS:

        feature_names.append(
            f"{signal}_{statistic}"
        )


ranking = sorted(
    zip(
        feature_names,
        model.feature_importances_
    ),
    key=lambda item: item[1],
    reverse=True
)


for name, score in ranking[:15]:

    print(
        f"{name:<32} "
        f"{score:.6f}"
    )


# =====================================================
# SAVE MODEL
# =====================================================

with open(
    MODEL_FILE,
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


print()
print(
    "Saved model:"
)

print(
    MODEL_FILE
)


# =====================================================
# FINISH
# =====================================================

print()
print("==============================================")
print("TRAINING COMPLETE")
print("==============================================")
