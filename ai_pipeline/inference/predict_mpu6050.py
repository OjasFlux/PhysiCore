import os
import pandas as pd
import numpy as np
import joblib


# =========================================================
# PATHS
# =========================================================

MODEL_FILE = (
    r"ai_pipeline\models\mpu6050_random_forest.pkl"
)


# =========================================================
# LABELS
# =========================================================

LABELS = {
    0: "Normal",
    1: "Minor_Fault",
    2: "Moderate_Fault",
    3: "Severe_Fault"
}


# =========================================================
# FEATURE EXTRACTION
# Same definitions used during training
# =========================================================

def extract_axis_features(signal):

    signal = np.asarray(
        signal,
        dtype=float
    )

    mean_value = np.mean(signal)

    std_value = np.std(signal)

    variance = np.var(signal)

    rms = np.sqrt(
        np.mean(signal ** 2)
    )

    maximum = np.max(signal)

    minimum = np.min(signal)

    peak_to_peak = (
        maximum - minimum
    )

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
# LOAD NEW FILE
# =========================================================

INPUT_FILE = input(
    "Enter new MPU6050 CSV path: "
).strip()


# =========================================================
# CHECK FILE
# =========================================================

if not os.path.exists(INPUT_FILE):

    raise FileNotFoundError(
        f"File not found: {INPUT_FILE}"
    )


# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading MPU6050 model...")

model = joblib.load(
    MODEL_FILE
)


# =========================================================
# LOAD SENSOR DATA
# =========================================================

print("Reading MPU6050 data...")

df = pd.read_csv(
    INPUT_FILE
)

print(
    "Samples:",
    len(df)
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

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
            f"Missing column: {column}"
        )


# =========================================================
# ACCELEROMETER FEATURES
# =========================================================

ax_features = extract_axis_features(
    df["Ax"].values
)

ay_features = extract_axis_features(
    df["Ay"].values
)

az_features = extract_axis_features(
    df["Az"].values
)


# =========================================================
# GYROSCOPE FEATURES
# =========================================================

gx_features = extract_axis_features(
    df["Gx"].values
)

gy_features = extract_axis_features(
    df["Gy"].values
)

gz_features = extract_axis_features(
    df["Gz"].values
)


# =========================================================
# MAGNITUDE FEATURES
# =========================================================

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


accel_mag_features = extract_axis_features(
    acceleration_magnitude
)

gyro_mag_features = extract_axis_features(
    gyroscope_magnitude
)


# =========================================================
# CREATE FEATURE VECTOR
# IMPORTANT:
# Keep the same order used during training.
# =========================================================

features = {}

for name, value in ax_features.items():
    features[f"Ax_{name}"] = value

for name, value in ay_features.items():
    features[f"Ay_{name}"] = value

for name, value in az_features.items():
    features[f"Az_{name}"] = value

for name, value in gx_features.items():
    features[f"Gx_{name}"] = value

for name, value in gy_features.items():
    features[f"Gy_{name}"] = value

for name, value in gz_features.items():
    features[f"Gz_{name}"] = value

for name, value in accel_mag_features.items():
    features[f"AccelMag_{name}"] = value

for name, value in gyro_mag_features.items():
    features[f"GyroMag_{name}"] = value


feature_df = pd.DataFrame(
    [features]
)


# =========================================================
# ALIGN FEATURE ORDER WITH MODEL
# =========================================================

if hasattr(
    model,
    "feature_names_in_"
):

    expected_features = list(
        model.feature_names_in_
    )

    missing_features = [
        name
        for name in expected_features
        if name not in feature_df.columns
    ]

    if missing_features:

        raise ValueError(
            "Missing model features: "
            + str(missing_features)
        )

    feature_df = feature_df[
        expected_features
    ]


# =========================================================
# PREDICTION
# =========================================================

prediction = model.predict(
    feature_df
)[0]

predicted_class = LABELS.get(
    int(prediction),
    "Unknown"
)


# =========================================================
# OUTPUT
# =========================================================

print("\n======================================")
print("MPU6050 FAULT PREDICTION")
print("======================================")

print(
    "Prediction:",
    predicted_class
)

print(
    "Class ID:",
    prediction
)


# =========================================================
# CONFIDENCE
# =========================================================

if hasattr(
    model,
    "predict_proba"
):

    probabilities = model.predict_proba(
        feature_df
    )[0]

    confidence = (
        probabilities[int(prediction)]
        * 100
    )

    print(
        f"Confidence: {confidence:.2f}%"
    )

print("======================================")
