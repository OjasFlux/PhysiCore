import os
import joblib
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================
# PATHS
# ==========================================

DATASET_FOLDER = r"ai_pipeline\training\dataset_split"
MODEL_FOLDER = r"ai_pipeline\models"

OUTPUT_MODEL = os.path.join(
    MODEL_FOLDER,
    "piezo_decision_tree.pkl"
)

# ==========================================
# LOAD DATA
# ==========================================

print("Loading dataset...")

X_train = pd.read_csv(
    os.path.join(DATASET_FOLDER, "X_train.csv")
)

y_train = pd.read_csv(
    os.path.join(DATASET_FOLDER, "y_train.csv")
).squeeze()

X_val = pd.read_csv(
    os.path.join(DATASET_FOLDER, "X_validation.csv")
)

y_val = pd.read_csv(
    os.path.join(DATASET_FOLDER, "y_validation.csv")
).squeeze()

X_test = pd.read_csv(
    os.path.join(DATASET_FOLDER, "X_test.csv")
)

y_test = pd.read_csv(
    os.path.join(DATASET_FOLDER, "y_test.csv")
).squeeze()

# ==========================================
# TRAIN SMALL DECISION TREE
# ==========================================

print("\nTraining Decision Tree...")

model = DecisionTreeClassifier(
    max_depth=5,
    min_samples_leaf=3,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# ==========================================
# VALIDATION
# ==========================================

val_prediction = model.predict(X_val)

val_accuracy = accuracy_score(
    y_val,
    val_prediction
)

val_precision = precision_score(
    y_val,
    val_prediction,
    average="weighted",
    zero_division=0
)

val_recall = recall_score(
    y_val,
    val_prediction,
    average="weighted",
    zero_division=0
)

val_f1 = f1_score(
    y_val,
    val_prediction,
    average="weighted",
    zero_division=0
)

# ==========================================
# TEST
# ==========================================

test_prediction = model.predict(X_test)

test_accuracy = accuracy_score(
    y_test,
    test_prediction
)

test_precision = precision_score(
    y_test,
    test_prediction,
    average="weighted",
    zero_division=0
)

test_recall = recall_score(
    y_test,
    test_prediction,
    average="weighted",
    zero_division=0
)

test_f1 = f1_score(
    y_test,
    test_prediction,
    average="weighted",
    zero_division=0
)

# ==========================================
# MODEL INFORMATION
# ==========================================

print("\n======================================")
print("DECISION TREE RESULTS")
print("======================================")

print("\nTree depth:")
print(model.get_depth())

print("\nNumber of leaves:")
print(model.get_n_leaves())

print("\nValidation:")
print(f"Accuracy  : {val_accuracy * 100:.2f}%")
print(f"Precision : {val_precision * 100:.2f}%")
print(f"Recall    : {val_recall * 100:.2f}%")
print(f"F1-score  : {val_f1 * 100:.2f}%")

print("\nTest:")
print(f"Accuracy  : {test_accuracy * 100:.2f}%")
print(f"Precision : {test_precision * 100:.2f}%")
print(f"Recall    : {test_recall * 100:.2f}%")
print(f"F1-score  : {test_f1 * 100:.2f}%")

# ==========================================
# SAVE MODEL
# ==========================================

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)

joblib.dump(
    model,
    OUTPUT_MODEL
)

print("\nModel saved to:")
print(OUTPUT_MODEL)
