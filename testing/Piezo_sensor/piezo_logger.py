import serial
import csv
import time

PORT = "COM7"          # Change to your Nano COM port
BAUD = 115200

filename = input("Enter filename (example: no_touch.csv): ")

print("Open Serial Port...")
ser = serial.Serial(PORT, BAUD, timeout=1)

# Nano resets automatically when the port opens
time.sleep(2)

# Remove startup garbage
ser.reset_input_buffer()

with open(filename, "w", newline="") as file:

    writer = csv.writer(file)
    writer.writerow(["Time_ms", "Piezo"])

    print("\nRecording...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:

            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) != 2:
                continue

            try:
                t = int(parts[0])
                v = int(parts[1])
            except ValueError:
                continue

            writer.writerow([t, v])
            print(f"{t},{v}")

    except KeyboardInterrupt:
        print("\nRecording Saved.")

ser.close()
