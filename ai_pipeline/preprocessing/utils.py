"""
Utility Functions
"""

from pathlib import Path


def is_csv(file_path: Path):
    return file_path.suffix.lower() == ".csv"


def count_rows(csv_file):

    with open(csv_file, "r", encoding="utf-8") as f:

        return sum(1 for _ in f) - 1


def write_report(report_path, text):

    with open(report_path, "a", encoding="utf-8") as f:

        f.write(text + "\n")
