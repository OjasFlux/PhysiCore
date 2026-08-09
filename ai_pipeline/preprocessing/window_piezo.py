import os
import pandas as pd

# =====================================================
# PATHS
# =====================================================

INPUT_ROOT = r"processed_dataset/Piezo_sensor"
OUTPUT_ROOT = r"windowed_dataset/Piezo_sensor"

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
# PROCESS EACH CLASS
# =====================================================

total_files = 0
total_windows = 0

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
            # READ PROCESSED CSV
            # -------------------------------------------------

            df = pd.read_csv(input_file)

            if "Time_ms" not in df.columns or "Piezo" not in df.columns:
                print(f"❌ Invalid columns: {filename}")
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

            print(f"❌ {filename} → {e}")

# =====================================================
# SUMMARY
# =====================================================

print("\n======================================")
print("PIEZO WINDOWING COMPLETED")
print("======================================")

print(f"Files processed : {total_files}")
print(f"Total windows   : {total_windows}")

print("\nOutput folder:")
print(OUTPUT_ROOT)
