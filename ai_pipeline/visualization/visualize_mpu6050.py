import os
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# PATHS
# =====================================================

DATASET_PATH = r"processed_dataset/MPU6050"
OUTPUT_PATH = r"ai_pipeline/visualization/outputs/MPU6050"

os.makedirs(OUTPUT_PATH, exist_ok=True)

# =====================================================
# CLASSES
# =====================================================

classes = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]

# =====================================================
# SENSOR COLUMNS
# =====================================================

sensor_columns = [
    "Ax",
    "Ay",
    "Az",
    "Gx",
    "Gy",
    "Gz"
]

# =====================================================
# PROCESS ALL CLASSES
# =====================================================

for class_name in classes:

    input_folder = os.path.join(DATASET_PATH, class_name)

    if not os.path.exists(input_folder):
        print(f"Skipping missing folder: {class_name}")
        continue

    output_folder = os.path.join(OUTPUT_PATH, class_name)
    os.makedirs(output_folder, exist_ok=True)

    print(f"\n========== {class_name} ==========")

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".csv")
    ]

    for filename in files:

        input_file = os.path.join(input_folder, filename)

        try:

            df = pd.read_csv(input_file)

            # Check columns
            required_columns = ["Time_ms"] + sensor_columns

            if not all(column in df.columns for column in required_columns):
                print(f"❌ Invalid columns: {filename}")
                continue

            # =================================================
            # 1. ACCELERATION PLOT
            # =================================================

            plt.figure(figsize=(10, 5))

            plt.plot(df["Time_ms"], df["Ax"], label="Ax")
            plt.plot(df["Time_ms"], df["Ay"], label="Ay")
            plt.plot(df["Time_ms"], df["Az"], label="Az")

            plt.title(
                f"MPU6050 Acceleration - {class_name} - {filename}"
            )

            plt.xlabel("Time (ms)")
            plt.ylabel("Acceleration")

            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            acceleration_file = os.path.join(
                output_folder,
                filename.replace(".csv", "_acceleration.png")
            )

            plt.savefig(acceleration_file, dpi=150)
            plt.close()

            # =================================================
            # 2. GYROSCOPE PLOT
            # =================================================

            plt.figure(figsize=(10, 5))

            plt.plot(df["Time_ms"], df["Gx"], label="Gx")
            plt.plot(df["Time_ms"], df["Gy"], label="Gy")
            plt.plot(df["Time_ms"], df["Gz"], label="Gz")

            plt.title(
                f"MPU6050 Gyroscope - {class_name} - {filename}"
            )

            plt.xlabel("Time (ms)")
            plt.ylabel("Angular Velocity")

            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            gyroscope_file = os.path.join(
                output_folder,
                filename.replace(".csv", "_gyroscope.png")
            )

            plt.savefig(gyroscope_file, dpi=150)
            plt.close()

            # =================================================
            # 3. INDIVIDUAL SENSOR PLOTS
            # =================================================

            for column in sensor_columns:

                plt.figure(figsize=(10, 4))

                plt.plot(
                    df["Time_ms"],
                    df[column]
                )

                plt.title(
                    f"MPU6050 {column} - "
                    f"{class_name} - {filename}"
                )

                plt.xlabel("Time (ms)")
                plt.ylabel(column)

                plt.grid(True)
                plt.tight_layout()

                output_file = os.path.join(
                    output_folder,
                    filename.replace(
                        ".csv",
                        f"_{column}.png"
                    )
                )

                plt.savefig(output_file, dpi=150)
                plt.close()

            print(f"✅ {filename}")

        except Exception as e:

            print(f"❌ {filename} -> {e}")

# =====================================================
# COMPLETE
# =====================================================

print("\n======================================")
print("MPU6050 VISUALIZATION COMPLETED")
print("======================================")

print("Plots saved in:")
print(OUTPUT_PATH)
