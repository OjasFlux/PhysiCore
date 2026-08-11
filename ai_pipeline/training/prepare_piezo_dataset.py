import pandas as pd
import os

# ==========================================
# PATHS
# ==========================================

INPUT_FILE = r"ai_pipeline\feature_extraction\piezo_features.csv"

OUTPUT_FILE = r"ai_pipeline\dataset_preparation\piezo_ml_dataset.csv"


# ==========================================
# LOAD DATA
# ==========================================

print("Loading feature dataset...")

df = pd.read_csv(INPUT_FILE)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# CHECK MISSING VALUES
# ==========================================

print("\nMissing values:")

print(df.isnull().sum())


# ==========================================
# CHECK DUPLICATES
# ==========================================

duplicates = df.duplicated().sum()

print("\nDuplicate rows:", duplicates)


# ==========================================
# REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates().reset_index(drop=True)


# ==========================================
# CHECK LABELS
# ==========================================

print("\nClass distribution:")

print(df["Label"].value_counts())


# ==========================================
# LABEL ENCODING
# ==========================================

label_mapping = {
    "Normal": 0,
    "Minor_Fault": 1,
    "Moderate_Fault": 2,
    "Severe_Fault": 3
}

df["Label_ID"] = df["Label"].map(label_mapping)


# ==========================================
# CHECK UNKNOWN LABELS
# ==========================================

unknown_labels = df[df["Label_ID"].isnull()]

if len(unknown_labels) > 0:

    print("\nWARNING: Unknown labels found:")
    print(unknown_labels["Label"].unique())

else:

    print("\nAll labels encoded successfully.")


# ==========================================
# SAVE
# ==========================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# FINAL INFORMATION
# ==========================================

print("\n====================================")
print("Dataset preparation completed")
print("====================================")

print("Final samples:", len(df))

print("\nFinal class distribution:")
print(df["Label"].value_counts())

print("\nLabel mapping:")
print(label_mapping)

print("\nSaved to:")
print(OUTPUT_FILE)