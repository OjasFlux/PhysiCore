import numpy as np
import pandas as pd


# =====================================================
# MPU6050 FEATURE ENGINEERING
#
# Input:
#   DataFrame containing 100 samples of:
#   Ax, Ay, Az, Gx, Gy, Gz
#
# Output:
#   Exactly 56 features
#
# 8 signals × 7 statistical features = 56
# =====================================================


FEATURE_NAMES = []


SIGNALS = [
    "Ax",
    "Ay",
    "Az",
    "Gx",
    "Gy",
    "Gz",
    "AccelMag",
    "GyroMag"
]


STATISTICS = [
    "Mean",
    "Std",
    "Variance",
    "RMS",
    "Maximum",
    "Minimum",
    "Peak_to_Peak"
]


# Build feature names
for signal in SIGNALS:

    for statistic in STATISTICS:

        FEATURE_NAMES.append(
            f"{signal}_{statistic}"
        )


# Safety check
if len(FEATURE_NAMES) != 56:

    raise RuntimeError(
        "MPU6050 feature list must contain exactly 56 features."
    )


# =====================================================
# EXTRACT 7 STATISTICAL FEATURES
# =====================================================

def extract_signal_features(
    signal
):
    """
    Extract seven statistical features from one signal.

    Returns:
        [
            mean,
            std,
            variance,
            rms,
            maximum,
            minimum,
            peak_to_peak
        ]
    """

    values = np.asarray(
        signal,
        dtype=np.float64
    )

    if values.size == 0:

        raise ValueError(
            "Signal is empty."
        )

    mean_value = np.mean(
        values
    )

    std_value = np.std(
        values,
        ddof=0
    )

    variance_value = np.var(
        values,
        ddof=0
    )

    rms_value = np.sqrt(
        np.mean(
            values * values
        )
    )

    maximum_value = np.max(
        values
    )

    minimum_value = np.min(
        values
    )

    peak_to_peak_value = (
        maximum_value -
        minimum_value
    )

    return [
        mean_value,
        std_value,
        variance_value,
        rms_value,
        maximum_value,
        minimum_value,
        peak_to_peak_value
    ]


# =====================================================
# VALIDATE INPUT
# =====================================================

def validate_mpu6050_dataframe(
    df
):
    """
    Validate an MPU6050 window.

    Required columns:
        Ax, Ay, Az, Gx, Gy, Gz

    Expected:
        100 samples
    """

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
                f"Missing required column: {column}"
            )

    if len(df) != 100:

        raise ValueError(
            "MPU6050 window must contain "
            f"100 samples, found {len(df)}."
        )

    for column in required_columns:

        values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if values.isna().any():

            raise ValueError(
                f"Invalid numeric values found in {column}."
            )


# =====================================================
# MAIN FEATURE EXTRACTION
# =====================================================

def extract_mpu6050_features(
    df
):
    """
    Extract exactly 56 MPU6050 features.

    Feature order:

    0-6:
        Ax

    7-13:
        Ay

    14-20:
        Az

    21-27:
        Gx

    28-34:
        Gy

    35-41:
        Gz

    42-48:
        AccelMag

    49-55:
        GyroMag
    """

    validate_mpu6050_dataframe(
        df
    )


    features = []


    # =================================================
    # SIX RAW AXES
    # =================================================

    raw_columns = [
        "Ax",
        "Ay",
        "Az",
        "Gx",
        "Gy",
        "Gz"
    ]


    for column in raw_columns:

        values = pd.to_numeric(
            df[column],
            errors="raise"
        ).to_numpy(
            dtype=np.float64
        )

        features.extend(
            extract_signal_features(
                values
            )
        )


    # =================================================
    # ACCELERATION MAGNITUDE
    #
    # sqrt(Ax² + Ay² + Az²)
    # =================================================

    ax = df["Ax"].to_numpy(
        dtype=np.float64
    )

    ay = df["Ay"].to_numpy(
        dtype=np.float64
    )

    az = df["Az"].to_numpy(
        dtype=np.float64
    )


    accel_magnitude = np.sqrt(
        ax * ax +
        ay * ay +
        az * az
    )


    features.extend(
        extract_signal_features(
            accel_magnitude
        )
    )


    # =================================================
    # GYROSCOPE MAGNITUDE
    #
    # sqrt(Gx² + Gy² + Gz²)
    # =================================================

    gx = df["Gx"].to_numpy(
        dtype=np.float64
    )

    gy = df["Gy"].to_numpy(
        dtype=np.float64
    )

    gz = df["Gz"].to_numpy(
        dtype=np.float64
    )


    gyro_magnitude = np.sqrt(
        gx * gx +
        gy * gy +
        gz * gz
    )


    features.extend(
        extract_signal_features(
            gyro_magnitude
        )
    )


    # =================================================
    # FINAL CHECK
    # =================================================

    if len(features) != 56:

        raise RuntimeError(
            "Feature extraction returned "
            f"{len(features)} features instead of 56."
        )


    return np.asarray(
        features,
        dtype=np.float64
    )


# =====================================================
# RETURN NAMED FEATURES
# =====================================================

def extract_mpu6050_feature_dict(
    df
):
    """
    Return the 56 features as a dictionary.

    Useful for:
        debugging
        visualization
        CSV export
        inspection
    """

    features = extract_mpu6050_features(
        df
    )

    return dict(
        zip(
            FEATURE_NAMES,
            features
        )
    )


# =====================================================
# TEST WHEN RUN DIRECTLY
# =====================================================

if __name__ == "__main__":

    print(
        "MPU6050 FEATURE ENGINEERING MODULE"
    )

    print(
        "Feature count:",
        len(FEATURE_NAMES)
    )

    print()

    for index, name in enumerate(
        FEATURE_NAMES
    ):

        print(
            f"{index:02d}  {name}"
        )
