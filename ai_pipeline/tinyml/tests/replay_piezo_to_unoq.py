import serial
import pandas as pd
import time

# ==========================================
# SETTINGS
# ==========================================

PORT = "COM7"       # CHANGE THIS
BAUD_RATE = 115200

INPUT_FILE = (
    r"windowed_dataset\Piezo_sensor"
    r"\Normal\normal_001_window_001.csv"
)

# ==========================================
# LOAD 100-SAMPLE WINDOW
# ==========================================

df = pd.read_csv(INPUT_FILE)

signal = df["Piezo"].astype(float).tolist()

if len(signal) != 100:
    raise ValueError(
        f"Expected 100 samples, got {len(signal)}"
    )

print("Loaded 100 samples.")

# ==========================================
# CONNECT TO UNO Q
# ==========================================

print("Connecting to UNO Q...")

ser = serial.Serial(
    PORT,
    BAUD_RATE,
    timeout=1
)

time.sleep(2)

ser.reset_input_buffer()

print("Sending samples...")

# ==========================================
# SEND
# ==========================================

for i, value in enumerate(signal):

    message = f"{value}\n"

    ser.write(
        message.encode()
    )

    time.sleep(0.005)

print("100 samples sent.")

# Give UNO Q time to calculate
time.sleep(2)

# ==========================================
# READ RESPONSE
# ==========================================

print("\nUNO Q response:\n")

while ser.in_waiting:

    line = ser.readline().decode(
        "utf-8",
        errors="ignore"
    ).strip()

    if line:
        print(line)

ser.close()

print("\nReplay completed.")
