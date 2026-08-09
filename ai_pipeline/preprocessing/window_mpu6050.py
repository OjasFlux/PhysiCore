import os
import pandas as pd

# =====================================================
# PATHS
# =====================================================

INPUT_ROOT = r"processed_dataset/MPU6050"
OUTPUT_ROOT = r"windowed_dataset/MPU6050"

# =====================================================
# WINDOW SETTINGS
# =====================================================

WINDOW_SIZE = 100
STEP_SIZE = 50

# =====================================================
# DATASET CLASSES
# =====================================================

classes = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]

# =====================================================
# EXPECTED COLUMNS
# =====================================================

EXPECTED_COLUMNS = [
    "Time_ms",
    "Ax",
    "Ay",
    "Az",
    "Gx",
    "Gy",
    "Gz"
]

# =====================================================
# COUNTERS
# =====================================================

total_files = 0
total_windows = 0
failed_files = 0

# =====================================================
# PROCESS ALL CLASSES
# =====================================================

for class_name in classes:

    input_folder = os.path.join(INPUT_ROOT, class_name)
    output_folder = os.path.join(OUTPUT_ROOT, class_name)

    if not os.path.exists(input_folder):
        print(f"Skipping missing folder: {class_name}")
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

        try:

            # -------------------------------------------------
            # READ CSV
            # -------------------------------------------------

            df = pd.read_csv(input_file)

            # -------------------------------------------------
            # CHECK COLUMNS
            # -------------------------------------------------

            if list(df.columns) != EXPECTED_COLUMNS:

                print(f"❌ Invalid columns: {filename}")
                failed_files += 1
                continue

            # -------------------------------------------------
            # CHECK WINDOW SIZE
            # -------------------------------------------------

            if len(df) < WINDOW_SIZE:

                print(
                    f"⚠️ Too short: {filename} "
                    f"({len(df)} samples)"
                )

                continue

            # -------------------------------------------------
            # CREATE WINDOWS
            # -------------------------------------------------

            window_number = 1

            for start in range(
                0,
                len(df) - WINDOW_SIZE + 1,
                STEP_SIZE
            ):

                end = start + WINDOW_SIZE

                window = df.iloc[start:end].copy()

                # -------------------------------------------------
                # SAVE WINDOW
                # -------------------------------------------------

                base_name = os.path.splitext(filename)[0]

                output_filename = (
                    f"{base_name}_window_{window_number:03d}.csv"
                )

                output_file = os.path.join(
                    output_folder,
                    output_filename
                )

                window.to_csv(
                    output_file,
                    index=False
                )

                window_number += 1
                total_windows += 1

            print(
                f"✅ {filename} → "
                f"{window_number - 1} windows"
            )

        except Exception as e:

            failed_files += 1

            print(f"❌ {filename} → {e}")

# =====================================================
# SUMMARY
# =====================================================

print("\n======================================")
print("MPU6050 WINDOWING COMPLETED")
print("======================================")

print(f"Files processed : {total_files}")
print(f"Failed files    : {failed_files}")
print(f"Total windows   : {total_windows}")

print("\nOutput folder:")
print(OUTPUT_ROOT)
