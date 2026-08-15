import os
import pandas as pd
import numpy as np


# =========================================================
# PATHS
# =========================================================

INPUT_FOLDER = r"windowed_dataset\MPU6050"

OUTPUT_FILE = (
    r"ai_pipeline\feature_engineering"
    r"\mpu6050_features.csv"
)


# =========================================================
# FEATURE FUNCTION
# =========================================================

def extract_axis_features(signal):
    signal = np.asarray(signal, dtype=float)

    mean_value = np.mean(signal)

    std_value = np.std(signal)

    variance = np.var(signal)

    rms = np.sqrt(
        np.mean(signal ** 2)
    )

    maximum = np.max(signal)

    minimum = np.min(signal)

    peak_to_peak = maximum - minimum

    return {
        "Mean": mean_value,
        "Std": std_value,
        "Variance": variance,
        "RMS": rms,
        "Maximum": maximum,
        "Minimum": minimum,
        "Peak_to_Peak": peak_to_peak
    }


# =========================================================
# PROCESS ONE MPU6050 WINDOW
# =========================================================

def extract_features(file_path, label):

    df = pd.read_csv(file_path)

    required_columns = [
        "Ax",
        "Ay",
        "Az",
        "Gx",
        "Gy",
        "Gz"
    ]

    for column in required_columns:

        if column not in df.columns:
            raise ValueError(
                f"Missing column '{column}' "
                f"in {file_path}"
            )

    # -----------------------------------------------------
    # Accelerometer features
    # -----------------------------------------------------

    ax_features = extract_axis_features(
        df["Ax"].values
    )

    ay_features = extract_axis_features(
        df["Ay"].values
    )

    az_features = extract_axis_features(
        df["Az"].values
    )

    # -----------------------------------------------------
    # Gyroscope features
    # -----------------------------------------------------

    gx_features = extract_axis_features(
        df["Gx"].values
    )

    gy_features = extract_axis_features(
        df["Gy"].values
    )

    gz_features = extract_axis_features(
        df["Gz"].values
    )

    # -----------------------------------------------------
    # Magnitudes
    # -----------------------------------------------------

    acceleration_magnitude = np.sqrt(
        df["Ax"].values ** 2 +
        df["Ay"].values ** 2 +
        df["Az"].values ** 2
    )

    gyroscope_magnitude = np.sqrt(
        df["Gx"].values ** 2 +
        df["Gy"].values ** 2 +
        df["Gz"].values ** 2
    )

    acceleration_mag_features = extract_axis_features(
        acceleration_magnitude
    )

    gyroscope_mag_features = extract_axis_features(
        gyroscope_magnitude
    )

    # -----------------------------------------------------
    # Combine all features
    # -----------------------------------------------------

    features = {}

    # Accelerometer
    for name, value in ax_features.items():
        features[f"Ax_{name}"] = value

    for name, value in ay_features.items():
        features[f"Ay_{name}"] = value

    for name, value in az_features.items():
        features[f"Az_{name}"] = value

    # Gyroscope
    for name, value in gx_features.items():
        features[f"Gx_{name}"] = value

    for name, value in gy_features.items():
        features[f"Gy_{name}"] = value

    for name, value in gz_features.items():
        features[f"Gz_{name}"] = value

    # Magnitudes
    for name, value in acceleration_mag_features.items():
        features[f"AccelMag_{name}"] = value

    for name, value in gyroscope_mag_features.items():
        features[f"GyroMag_{name}"] = value

    # Label and file information
    features["Label"] = label
    features["File"] = os.path.basename(file_path)

    return features


# =========================================================
# PROCESS DATASET
# =========================================================

all_features = []

print("Starting MPU6050 feature extraction...\n")

for label in os.listdir(INPUT_FOLDER):

    label_folder = os.path.join(
        INPUT_FOLDER,
        label
    )

    if not os.path.isdir(label_folder):
        continue

    print("Processing:", label)

    for filename in os.listdir(label_folder):

        if not filename.lower().endswith(".csv"):
            continue

        file_path = os.path.join(
            label_folder,
            filename
        )

        try:

            features = extract_features(
                file_path,
                label
            )

            all_features.append(features)

        except Exception as error:

            print(
                "Error processing",
                filename,
                ":",
                error
            )


# =========================================================
# CREATE DATAFRAME
# =========================================================

if len(all_features) == 0:

    print("\nNo MPU6050 windows found.")
    print(
        "Check this folder:",
        INPUT_FOLDER
    )

else:

    features_df = pd.DataFrame(
        all_features
    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    features_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print("\n======================================")
    print("MPU6050 FEATURE EXTRACTION COMPLETED")
    print("======================================")

    print(
        "Total windows:",
        len(features_df)
    )

    print(
        "Total columns:",
        len(features_df.columns)
    )

    print("\nClass distribution:")

    print(
        features_df["Label"].value_counts()
    )

    print("\nFirst 5 rows:")

    print(
        features_df.head()
    )

    print("\nSaved to:")

    print(OUTPUT_FILE)
