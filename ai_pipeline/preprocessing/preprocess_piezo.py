"""
PhysiCore
Piezo Dataset Preprocessing

Version : 1.0

Tasks
------
1. Read CSV
2. Remove empty rows
3. Remove duplicate rows
4. Reset timestamp to start at 0 ms
5. Save processed CSV
"""

import os
import pandas as pd

# =====================================================
# INPUT / OUTPUT PATHS
# =====================================================

filename = input("Enter CSV filename (e.g. Normal_001.csv): ")

INPUT_FILE = rf"dataset/Piezo_sensor/Normal/{filename}"

OUTPUT_FOLDER = r"processed_dataset/Piezo_sensor/Normal"

OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, filename)

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =====================================================
# READ CSV
# =====================================================

print("Reading CSV...")

df = pd.read_csv(INPUT_FILE)

# =====================================================
# DATASET INFORMATION
# =====================================================

print("\nDataset Information")
print("---------------------------")
print(df.info())

print("\nFirst 5 Rows")
print(df.head())

print("\nTotal Samples :", len(df))

# =====================================================
# REMOVE EMPTY ROWS
# =====================================================

before = len(df)

df = df.dropna()

after = len(df)

print(f"\nRemoved Empty Rows : {before-after}")

# =====================================================
# REMOVE DUPLICATE ROWS
# =====================================================

before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"Removed Duplicate Rows : {before-after}")

# =====================================================
# RESET TIMESTAMP
# =====================================================

print("\nResetting Timestamp...")

df["Time_ms"] = df["Time_ms"] - df["Time_ms"].iloc[0]

# =====================================================
# VERIFY
# =====================================================

print("\nTimestamp Preview")

print(df.head())

# =====================================================
# SAVE
# =====================================================

df.to_csv(OUTPUT_FILE, index=False)

print("\n=================================")
print("Preprocessing Completed")
print("Saved :", OUTPUT_FILE)
print("=================================")
