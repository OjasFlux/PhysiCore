import os
import pandas as pd

# =====================================================
# PATHS
# =====================================================

INPUT_ROOT = r"dataset/MPU6050"
OUTPUT_ROOT = r"processed_dataset/MPU6050"

# =====================================================
# DATASET CLASSES
# =====================================================

classes = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]

EXPECTED_COLUMNS = [
    "Time_ms",
    "Ax",
    "Ay",
    "Az",
    "Gx",
    "Gy",
    "Gz"
]

total_files = 0
processed_files = 0
failed_files = 0

# =====================================================
# PROCESS ALL CLASSES
# =====================================================

for class_name in classes:

    input_folder = os.path.join(INPUT_ROOT, class_name)
    output_folder = os.path.join(OUTPUT_ROOT, class_name)

    if not os.path.exists(input_folder):
        print(f"\nSkipping missing folder: {class_name}")
        continue

    os.makedirs(output_folder, exist_ok=True)

    print(f"\n========== {class_name} ==========")

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".csv")
    ]

    for filename in files:

        total_files += 1

        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename)

        try:

            # -------------------------------------------------
            # READ CSV
            # -------------------------------------------------

            df = pd.read_csv(input_file)

            # -------------------------------------------------
            # CHECK COLUMNS
            # -------------------------------------------------

            if list(df.columns) != EXPECTED_COLUMNS:

                print(f"❌ Wrong columns: {filename}")
                failed_files += 1
                continue

            # -------------------------------------------------
            # REMOVE MISSING VALUES
            # -------------------------------------------------

            before = len(df)

            df = df.dropna()

            removed_missing = before - len(df)

            # -------------------------------------------------
            # REMOVE DUPLICATES
            # -------------------------------------------------

            before = len(df)

            df = df.drop_duplicates()

            removed_duplicates = before - len(df)

            # -------------------------------------------------
            # RESET TIMESTAMP
            # -------------------------------------------------

            if len(df) > 0:

                df["Time_ms"] = (
                    df["Time_ms"] - df["Time_ms"].iloc[0]
                )

            # -------------------------------------------------
            # SAVE
            # -------------------------------------------------

            df.to_csv(output_file, index=False)

            processed_files += 1

            print(
                f"✅ {filename} | "
                f"Samples: {len(df)} | "
                f"Missing removed: {removed_missing} | "
                f"Duplicates removed: {removed_duplicates}"
            )

        except Exception as e:

            failed_files += 1

            print(f"❌ {filename} -> {e}")

# =====================================================
# SUMMARY
# =====================================================

print("\n======================================")
print("MPU6050 PREPROCESSING COMPLETED")
print("======================================")

print(f"Total files     : {total_files}")
print(f"Processed files : {processed_files}")
print(f"Failed files    : {failed_files}")

print("\nOutput folder:")
print(OUTPUT_ROOT)
