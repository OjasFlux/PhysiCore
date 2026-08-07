"""
PhysiCore
Configuration File
"""

from pathlib import Path

# ==========================================================
# DATASET PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATASET_PATH = PROJECT_ROOT / "dataset"

REPORT_PATH = Path(__file__).resolve().parent / "reports"

REPORT_PATH.mkdir(exist_ok=True)

# ==========================================================
# SUPPORTED SENSORS
# ==========================================================

SENSORS = {
    "Piezo_sensor": [
        "Time_ms",
        "Piezo"
    ],

    "MPU6050": [
        "Time_ms",
        "Ax",
        "Ay",
        "Az",
        "Gx",
        "Gy",
        "Gz"
    ],

    "Microphone": [
        "Time_ms",
        "Microphone"
    ]
}

# ==========================================================
# CLASS LABELS
# ==========================================================

CLASSES = [
    "Normal",
    "Minor_Fault",
    "Moderate_Fault",
    "Severe_Fault"
]

# ==========================================================
# SAMPLE LIMITS
# ==========================================================

MIN_ROWS = 300
MAX_ROWS = 1200

# ==========================================================
# VALID FILE EXTENSION
# ==========================================================

VALID_EXTENSION = ".csv"
