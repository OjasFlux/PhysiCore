import os
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# PATHS
# =====================================================

DATASET_PATH = r"processed_dataset/Piezo_sensor"
OUTPUT_PATH = r"ai_pipeline/visualization/outputs/Piezo"

# Create output folder
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
# PROCESS EACH CLASS
# =====================================================

for class_name in classes:

    input_folder = os.path.join(DATASET_PATH, class_name)

    if not os.path.exists(input_folder):
        print(f"Skipping: {class_name}")
        continue

    output_folder = os.path.join(OUTPUT_PATH, class_name)
    os.makedirs(output_folder, exist_ok=True)

    print(f"\nProcessing {class_name}...")

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".csv")
    ]

    for filename in files:

        input_file = os.path.join(input_folder, filename)

        try:
            df = pd.read_csv(input_file)

            # Check required columns
            if "Time_ms" not in df.columns or "Piezo" not in df.columns:
                print(f"❌ Invalid columns: {filename}")
                continue

            # =================================================
            # PLOT
            # =================================================

            plt.figure(figsize=(10, 5))

            plt.plot(
                df["Time_ms"],
                df["Piezo"],
                linewidth=1
            )

            plt.title(f"Piezo Signal - {class_name} - {filename}")
            plt.xlabel("Time (ms)")
            plt.ylabel("Piezo Value")

            plt.grid(True)

            plt.tight_layout()

            # =================================================
            # SAVE
            # =================================================

            output_file = os.path.join(
                output_folder,
                filename.replace(".csv", ".png")
            )

            plt.savefig(output_file, dpi=150)

            plt.close()

            print(f"✅ {filename}")

        except Exception as e:

            print(f"❌ {filename}: {e}")

# =====================================================
# COMPLETE
# =====================================================

print("\n====================================")
print("PIEZO VISUALIZATION COMPLETED")
print("====================================")

print(f"Plots saved in:")
print(OUTPUT_PATH)
