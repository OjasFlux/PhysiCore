import os
import pandas as pd

from sklearn.model_selection import train_test_split

# ==========================================
# PATHS
# ==========================================

INPUT_FILE = r"ai_pipeline\training\mpu6050_ml_dataset.csv"

OUTPUT_FOLDER = r"ai_pipeline\training\mpu6050_dataset_split"

# ==========================================
# LOAD DATA
# ==========================================

print("Loading MPU6050 dataset...")

df = pd.read_csv(INPUT_FILE)

print("Total samples:", len(df))

# ==========================================
# FEATURES AND LABEL
# ==========================================

X = df.drop(
    columns=["Label", "Label_ID", "File"]
)

y = df["Label_ID"]

print("Features:", X.shape[1])

# ==========================================
# TRAIN / TEMP
# ==========================================

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

# ==========================================
# VALIDATION / TEST
# ==========================================

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)

# ==========================================
# CREATE OUTPUT
# ==========================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

# ==========================================
# SAVE DATA
# ==========================================

X_train.to_csv(
    os.path.join(
        OUTPUT_FOLDER,
        "X_train.csv"
    ),
    index=False
)

X_val.to_csv(
    os.path.join(
        OUTPUT_FOLDER,
        "X_validation.csv"
    ),
    index=False
)

X_test.to_csv(
    os.path.join(
        OUTPUT_FOLDER,
        "X_test.csv"
    ),
    index=False
)

y_train.to_csv(
    os.path.join(
        OUTPUT_FOLDER,
        "y_train.csv"
    ),
    index=False
)

y_val.to_csv(
    os.path.join(
        OUTPUT_FOLDER,
        "y_validation.csv"
    ),
    index=False
)

y_test.to_csv(
    os.path.join(
        OUTPUT_FOLDER,
        "y_test.csv"
    ),
    index=False
)

# ==========================================
# RESULTS
# ==========================================

print("\n======================================")
print("MPU6050 DATASET SPLIT COMPLETED")
print("======================================")

print("Training samples   :", len(X_train))
print("Validation samples :", len(X_val))
print("Testing samples    :", len(X_test))

print("\nSplit ratio:")
print("Train      : 70%")
print("Validation : 15%")
print("Test       : 15%")

print("\nSaved to:")
print(OUTPUT_FOLDER)