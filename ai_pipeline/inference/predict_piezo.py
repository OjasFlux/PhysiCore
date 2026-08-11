import pandas as pd
import numpy as np
import joblib

from scipy.fft import rfft, rfftfreq


# =========================================================
# SETTINGS
# =========================================================

MODEL_FILE = r"ai_pipeline\models\piezo_random_forest.pkl"

SAMPLE_RATE = 50

LABELS = {
    0: "Normal",
    1: "Minor_Fault",
    2: "Moderate_Fault",
    3: "Severe_Fault"
}


# =========================================================
# GET NEW FILE
# =========================================================

INPUT_FILE = input(
    "Enter new Piezo CSV path: "
).strip()


# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading trained model...")

model = joblib.load(MODEL_FILE)


# =========================================================
# LOAD CSV
# =========================================================

print("Reading Piezo data...")

df = pd.read_csv(INPUT_FILE)

signal = df["Piezo"].values.astype(float)

print("Samples:", len(signal))


# =========================================================
# FEATURE EXTRACTION
# SAME FEATURES USED DURING TRAINING
# =========================================================

mean_value = np.mean(signal)

std_value = np.std(signal)

variance = np.var(signal)

rms = np.sqrt(
    np.mean(signal ** 2)
)

maximum = np.max(signal)

minimum = np.min(signal)

peak_to_peak = maximum - minimum


# =========================================================
# FFT FEATURES
# =========================================================

signal_centered = signal - mean_value

fft_values = np.abs(
    rfft(signal_centered)
)

frequencies = rfftfreq(
    len(signal_centered),
    1 / SAMPLE_RATE
)

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


# =========================================================
# CREATE FEATURE DATAFRAME
# =========================================================

features = pd.DataFrame([{

    "Mean": mean_value,

    "Std": std_value,

    "Variance": variance,

    "RMS": rms,

    "Maximum": maximum,

    "Minimum": minimum,

    "Peak_to_Peak": peak_to_peak,

    "Dominant_Frequency": dominant_frequency,

    "Spectral_Energy": spectral_energy

}])


# =========================================================
# PREDICT
# =========================================================

prediction = model.predict(features)[0]

predicted_class = LABELS.get(
    int(prediction),
    "Unknown"
)


# =========================================================
# RESULT
# =========================================================

print("\n================================")
print("PIEZO FAULT PREDICTION")
print("================================")

print("Prediction:", predicted_class)

print("Class ID:", prediction)


# =========================================================
# CONFIDENCE
# =========================================================

if hasattr(model, "predict_proba"):

    probabilities = model.predict_proba(
        features
    )[0]

    confidence = probabilities[
        int(prediction)
    ] * 100

    print(
        f"Confidence: {confidence:.2f}%"
    )

print("================================")
