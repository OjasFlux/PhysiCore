import pandas as pd
import numpy as np
import os
from scipy.fft import rfft, rfftfreq

# =========================================================
# PATHS
# =========================================================

INPUT_FOLDER = r"windowed_dataset\Piezo_sensor"
OUTPUT_FILE = r"ai_pipeline\feature_extraction\piezo_features.csv"

# Sampling rate from your Piezo data
# ~20 ms between samples = about 50 Hz
SAMPLE_RATE = 50

# =========================================================
# FEATURE EXTRACTION
# =========================================================

def extract_features(file_path, label):

    df = pd.read_csv(file_path)

    signal = df["Piezo"].values.astype(float)

    if len(signal) == 0:
        return None

    # -----------------------------
    # Time-domain features
    # -----------------------------

    mean_value = np.mean(signal)

    std_value = np.std(signal)

    variance = np.var(signal)

    rms = np.sqrt(np.mean(signal ** 2))

    maximum = np.max(signal)

    minimum = np.min(signal)

    peak_to_peak = maximum - minimum

    # -----------------------------
    # Frequency-domain features
    # -----------------------------

    signal_centered = signal - mean_value

    fft_values = np.abs(rfft(signal_centered))

    frequencies = rfftfreq(
        len(signal_centered),
        1 / SAMPLE_RATE
    )

    # Ignore DC component
    if len(fft_values) > 1:

        fft_values[0] = 0

        dominant_frequency = frequencies[
            np.argmax(fft_values)
        ]

        spectral_energy = np.sum(
            fft_values ** 2
        )

    else:

        dominant_frequency = 0

        spectral_energy = 0

    # -----------------------------
    # Return features
    # -----------------------------

    return {
        "Mean": mean_value,
        "Std": std_value,
        "Variance": variance,
        "RMS": rms,
        "Maximum": maximum,
        "Minimum": minimum,
        "Peak_to_Peak": peak_to_peak,
        "Dominant_Frequency": dominant_frequency,
        "Spectral_Energy": spectral_energy,
        "Label": label
    }


# =========================================================
# PROCESS DATASET
# =========================================================

all_features = []

print("Starting Piezo feature extraction...\n")

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

            if features is not None:

                features["File"] = filename

                all_features.append(features)

        except Exception as e:

            print(
                "Error processing",
                filename,
                ":",
                e
            )


# =========================================================
# SAVE
# =========================================================

if len(all_features) == 0:

    print("\nNo feature data found.")
    print("Check your INPUT_FOLDER path.")

else:

    features_df = pd.DataFrame(
        all_features
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    features_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n================================")
    print("Feature extraction completed")
    print("================================")

    print(
        "Total windows:",
        len(features_df)
    )

    print(
        "Features:",
        len(features_df.columns)
    )

    print("\nPreview:")
    print(features_df.head())

    print(
        "\nSaved to:",
        OUTPUT_FILE
    )
