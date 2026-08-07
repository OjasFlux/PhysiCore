from pathlib import Path
import pandas as pd

from config import *
from utils import *

REPORT = REPORT_PATH / "validation_report.txt"

# Clear old report
REPORT.write_text("")

write_report(REPORT, "=" * 50)
write_report(REPORT, "PHYSICORE DATASET VALIDATION REPORT")
write_report(REPORT, "=" * 50)
write_report(REPORT, "")

for sensor, expected_header in SENSORS.items():

    sensor_path = DATASET_PATH / sensor

    write_report(REPORT, f"\nSensor : {sensor}")

    if not sensor_path.exists():

        write_report(REPORT, "ERROR : Folder Missing")

        continue

    total = 0

    passed = 0

    warnings = 0

    for cls in CLASSES:

        class_path = sensor_path / cls

        if not class_path.exists():

            write_report(REPORT, f"Missing Class Folder : {cls}")

            continue

        for file in class_path.glob("*.csv"):

            total += 1

            try:

                df = pd.read_csv(file)

                if list(df.columns) != expected_header:

                    write_report(
                        REPORT,
                        f"Header Error : {file.name}"
                    )

                    warnings += 1

                    continue

                rows = len(df)

                if rows < MIN_ROWS or rows > MAX_ROWS:

                    write_report(
                        REPORT,
                        f"Sample Warning : {file.name} ({rows} rows)"
                    )

                    warnings += 1

                else:

                    passed += 1

            except Exception as e:

                write_report(
                    REPORT,
                    f"ERROR : {file.name} : {e}"
                )

    write_report(REPORT, "")
    write_report(REPORT, f"Files : {total}")
    write_report(REPORT, f"Passed : {passed}")
    write_report(REPORT, f"Warnings : {warnings}")
    write_report(REPORT, "-" * 50)

print("\nValidation Complete!")
print("Report saved to:")
print(REPORT)
