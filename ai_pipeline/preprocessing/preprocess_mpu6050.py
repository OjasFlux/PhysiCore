import os
import glob
import pandas as pd

# =====================================================
# SETTINGS
# =====================================================

INPUT_ROOT = r"dataset\MPU6050_NEW"
OUTPUT_ROOT = r"windowed_dataset\MPU6050_NEW"

WINDOW_SIZE = 100
STEP_SIZE = 100

CLASSES = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]

REQUIRED_COLUMNS = [
    "Time_ms",
    "Ax",
    "Ay",
    "Az",
    "Gx",
    "Gy",
    "Gz"
]


# =====================================================
# CHECK INPUT
# =====================================================

print()
print("MPU6050 NEW DATASET PREPROCESSING")
print("Input :", INPUT_ROOT)
print("Output:", OUTPUT_ROOT)
print("Window:", WINDOW_SIZE)
print("Step  :", STEP_SIZE)
print()

if not os.path.isdir(INPUT_ROOT):
    raise FileNotFoundError(
        "Input folder not found:\n" + INPUT_ROOT
    )


# =====================================================
# GLOBAL COUNTERS
# =====================================================

total_files = 0
total_windows = 0


# =====================================================
# PROCESS CLASSES
# =====================================================

for class_name in CLASSES:

    input_folder = os.path.join(
        INPUT_ROOT,
        class_name
    )

    output_folder = os.path.join(
        OUTPUT_ROOT,
        class_name
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    if not os.path.isdir(input_folder):

        print(
            "WARNING: folder not found:",
            input_folder
        )

        continue

    csv_files = sorted(
        glob.glob(
            os.path.join(
                input_folder,
                "*.csv"
            )
        )
    )

    print()
    print("CLASS:", class_name)
    print("FILES:", len(csv_files))

    class_windows = 0

    # =================================================
    # PROCESS EACH CSV
    # =================================================

    for file_path in csv_files:

        filename = os.path.basename(
            file_path
        )

        print(
            "Processing:",
            filename
        )

        total_files += 1

        # ---------------------------------------------
        # READ
        # ---------------------------------------------

        try:

            df = pd.read_csv(
                file_path
            )

        except Exception as error:

            print(
                "ERROR reading:",
                file_path
            )

            print(
                error
            )

            continue

        # ---------------------------------------------
        # CHECK COLUMNS
        # ---------------------------------------------

        missing = []

        for column in REQUIRED_COLUMNS:

            if column not in df.columns:
                missing.append(column)

        if missing:

            print(
                "Missing columns:",
                missing
            )

            continue

        # ---------------------------------------------
        # KEEP REQUIRED COLUMNS
        # ---------------------------------------------

        df = df[
            REQUIRED_COLUMNS
        ].copy()

        # ---------------------------------------------
        # CONVERT TO NUMERIC
        # ---------------------------------------------

        for column in REQUIRED_COLUMNS:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        # ---------------------------------------------
        # REMOVE INVALID ROWS
        # ---------------------------------------------

        before = len(df)

        df = df.dropna()

        removed = (
            before -
            len(df)
        )

        if removed > 0:

            print(
                "Removed invalid rows:",
                removed
            )

        sample_count = len(df)

        print(
            "Samples:",
            sample_count
        )

        # ---------------------------------------------
        # CHECK SIZE
        # ---------------------------------------------

        if sample_count < WINDOW_SIZE:

            print(
                "Not enough samples for a window."
            )

            continue

        # ---------------------------------------------
        # WINDOW
        # ---------------------------------------------

        window_number = 1

        start = 0

        while (
            start + WINDOW_SIZE
            <= sample_count
        ):

            end = (
                start +
                WINDOW_SIZE
            )

            window_df = df.iloc[
                start:end
            ].copy()

            # -----------------------------------------
            # RESET TIME
            # -----------------------------------------

            first_time = float(
                window_df[
                    "Time_ms"
                ].iloc[0]
            )

            window_df["Time_ms"] = (
                window_df["Time_ms"]
                - first_time
            )

            # -----------------------------------------
            # OUTPUT NAME
            # -----------------------------------------

            base_name = os.path.splitext(
                filename
            )[0]

            output_name = (
                base_name
                + "_window_"
                + f"{window_number:03d}.csv"
            )

            output_path = os.path.join(
                output_folder,
                output_name
            )

            # -----------------------------------------
            # SAVE
            # -----------------------------------------

            window_df.to_csv(
                output_path,
                index=False
            )

            window_number += 1
            class_windows += 1
            total_windows += 1

            start += STEP_SIZE

    print(
        "Windows created:",
        class_windows
    )


# =====================================================
# FINAL
# =====================================================

print()
print("PREPROCESSING COMPLETED")
print("Raw files:", total_files)
print("Windows  :", total_windows)
print("Output   :", OUTPUT_ROOT)
print()
