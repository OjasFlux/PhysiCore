import os
import joblib

# ==========================================
# MODEL PATH
# ==========================================

MODEL_FILE = r"ai_pipeline\models\piezo_random_forest.pkl"


# ==========================================
# CHECK MODEL FILE
# ==========================================

if not os.path.exists(MODEL_FILE):
    print("Model file not found:")
    print(MODEL_FILE)
    exit()


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading Piezo model...")

model = joblib.load(MODEL_FILE)


# ==========================================
# MODEL INFORMATION
# ==========================================

print("\n========================================")
print("PIEZO MODEL ANALYSIS")
print("========================================")

print("\nModel type:")
print(type(model).__name__)

print("\nNumber of trees:")
print(model.n_estimators)

print("\nNumber of input features:")
print(model.n_features_in_)

print("\nNumber of classes:")
print(model.n_classes_)

print("\nClasses:")
print(model.classes_)

print("\nMaximum tree depth:")

depths = []

for tree in model.estimators_:
    depths.append(tree.tree_.max_depth)

print(max(depths))

print("\nAverage tree depth:")
print(sum(depths) / len(depths))

print("\nMinimum tree depth:")
print(min(depths))


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print("\n========================================")
print("FEATURE IMPORTANCE")
print("========================================")

feature_names = [
    "Mean",
    "Std",
    "Variance",
    "RMS",
    "Maximum",
    "Minimum",
    "Peak_to_Peak",
    "Dominant_Frequency",
    "Spectral_Energy"
]

for name, importance in zip(
    feature_names,
    model.feature_importances_
):

    print(
        f"{name:25s}: {importance:.6f}"
    )


# ==========================================
# MODEL FILE SIZE
# ==========================================

file_size = os.path.getsize(MODEL_FILE)

file_size_kb = file_size / 1024
file_size_mb = file_size_kb / 1024

print("\n========================================")
print("MODEL SIZE")
print("========================================")

print(f"Bytes : {file_size}")
print(f"KB    : {file_size_kb:.2f}")
print(f"MB    : {file_size_mb:.2f}")


# ==========================================
# SUMMARY
# ==========================================

print("\n========================================")
print("ANALYSIS COMPLETED")
print("========================================")

print("Model :", MODEL_FILE)
print("Trees :", model.n_estimators)
print("Features :", model.n_features_in_)
print("Classes :", model.n_classes_)
print(f"Size : {file_size_kb:.2f} KB")

print("\nNext step:")
print("Determine whether the model is suitable")
print("for embedded TinyML deployment.")
