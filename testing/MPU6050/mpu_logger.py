import serial
import csv
import time
import os

# -----------------------------
# Configuration
# -----------------------------
PORT = "COM7"          # Change to your Arduino COM Port
BAUD = 115200

filename = input("Enter filename (Example: Normal_001.csv): ")

os.makedirs("Dataset/MPU6050", exist_ok=True)

filepath = os.path.join("Dataset", "MPU6050", filename)

# -----------------------------
# Open Serial Port
# -----------------------------
ser = serial.Serial(PORT, BAUD)

print("Connecting to Arduino...")
time.sleep(2)

# Clear old serial data
ser.reset_input_buffer()

print("Recording...")
print("Press CTRL+C to Stop\n")

# -----------------------------
# Save CSV
# -----------------------------
with open(filepath, "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Time_ms",
        "Ax",
        "Ay",
        "Az",
        "Gx",
        "Gy",
        "Gz"
    ])

    first_time = None

    try:

        while True:

            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            data = line.split(",")

            if len(data) != 7:
                continue

            try:

                t = int(float(data[0]))

                if first_time is None:
                    first_time = t

                t = t - first_time

                row = [
                    t,
                    float(data[1]),
                    float(data[2]),
                    float(data[3]),
                    float(data[4]),
                    float(data[5]),
                    float(data[6])
                ]

                writer.writerow(row)

                print(row)

            except:
                continue

    except KeyboardInterrupt:
        print("\nRecording Saved!")

ser.close()
