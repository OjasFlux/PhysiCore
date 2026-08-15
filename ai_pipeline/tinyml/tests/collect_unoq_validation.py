import serial
import csv
import os
import time

# ==========================================
# SETTINGS
# ==========================================

PORT = "COM7"          # CHANGE THIS
BAUD_RATE = 115200

TOTAL_WINDOWS = 50

OUTPUT_FOLDER = r"ai_pipeline\tinyml\tests"

# ==========================================
# EXPECTED CLASS
# ==========================================

print("\nSelect actual machine condition:")

print("0 = Normal")
print("1 = Minor Fault")
print("2 = Moderate Fault")
print("3 = Severe Fault")

expected_class = int(
    input("Enter expected class: ")
)

class_names = {
    0: "Normal",
    1: "Minor_Fault",
    2: "Moderate_Fault",
    3: "Severe_Fault"
}

expected_name = class_names[
    expected_class
]

# ==========================================
# OUTPUT FILE
# ==========================================

filename = input(
    "Enter output filename "
    "(Example: normal_validation.csv): "
).strip()

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

output_file = os.path.join(
    OUTPUT_FOLDER,
    filename
)

# ==========================================
# CONNECT
# ==========================================

print("\nConnecting to UNO Q...")

ser = serial.Serial(
    PORT,
    BAUD_RATE,
    timeout=2
)

time.sleep(2)

ser.reset_input_buffer()

print("\nRecording:")
print("Condition:", expected_name)
print("Windows:", TOTAL_WINDOWS)
print("Press CTRL+C to stop\n")

# ==========================================
# CSV HEADER
# ==========================================

with open(
    output_file,
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Window",
        "Mean",
        "Std",
        "Variance",
        "RMS",
        "Maximum",
        "Minimum",
        "Peak_to_Peak",
        "Dominant_Frequency",
        "Spectral_Energy",
        "Prediction",
        "Expected"
    ])

    count = 0

    try:

        while count < TOTAL_WINDOWS:

            line = ser.readline().decode(
                "utf-8",
                errors="ignore"
            ).strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) != 11:
                continue

            try:

                window = int(parts[0])
                mean = float(parts[1])
                std = float(parts[2])
                variance = float(parts[3])
                rms = float(parts[4])
                maximum = float(parts[5])
                minimum = float(parts[6])
                p2p = float(parts[7])
                frequency = float(parts[8])
                energy = float(parts[9])
                prediction = int(parts[10])

            except ValueError:
                continue

            writer.writerow([
                window,
                mean,
                std,
                variance,
                rms,
                maximum,
                minimum,
                p2p,
                frequency,
                energy,
                prediction,
                expected_class
            ])

            count += 1

            result = (
                "CORRECT"
                if prediction == expected_class
                else "WRONG"
            )

            print(
                f"{count}/{TOTAL_WINDOWS} "
                f"Prediction={class_names.get(prediction, 'Unknown')} "
                f"Expected={expected_name} "
                f"[{result}]"
            )

    except KeyboardInterrupt:

        print("\nStopped manually.")

    finally:

        ser.close()

print("\n================================")
print("VALIDATION RECORDING SAVED")
print("================================")

print("File:", output_file)
print("Windows:", count)
print("Expected:", expected_name)