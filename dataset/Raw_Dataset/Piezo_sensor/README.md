# Piezo Sensor Dataset Collection Guide

## Project

**PhysiCore**
AI-Based Intelligent Machine Fault Detection System

---

# Objective

This dataset contains vibration data collected using a Piezo Vibration Sensor for training and validating the AI model.

The objective is to classify machine conditions into four categories:

- Normal
- Minor Fault
- Moderate Fault
- Severe Fault

---

# Sensor Information

| Item | Details |
|------|---------|
| Sensor | Piezo Vibration Sensor |
| Microcontroller | Arduino UNO Q|
| Sampling Interval | 20 ms |
| Sampling Rate | ~50 Hz |
| Output | Analog Value (0–1023) |
| File Format | CSV |

---

# Dataset Structure

```
dataset/
└── Piezo_sensor/
    ├── Normal/
    ├── Minor_Fault/
    ├── Moderate_Fault/
    └── Severe_Fault/
```

---

# CSV Format

Each CSV file contains two columns.

```
Time_ms,Piezo
0,2
20,1
40,3
60,215
80,480
100,5
```

## Columns

| Column | Description |
|---------|-------------|
| Time_ms | Time elapsed from the beginning of the recording |
| Piezo | Raw analog sensor value |

---

# Data Collection Procedure

## Normal

Purpose:

Collect background vibration without any external disturbance.

Procedure:

1. Place the sensor on the machine or test surface.
2. Start recording.
3. Do NOT touch the sensor.
4. Record for approximately 10–15 seconds.
5. Save the CSV file.

Expected Data:

- Stable readings
- Small fluctuations only
- No intentional impacts

---

## Minor Fault

Purpose:

Simulate a small vibration or light mechanical fault.

Procedure:

1. Start recording.
2. Wait about 3–5 seconds.
3. Apply one light tap or small vibration.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Data:

- Small vibration peak
- Returns to normal after the event

---

## Moderate Fault

Purpose:

Simulate a medium mechanical impact.

Procedure:

1. Start recording.
2. Wait about 3–5 seconds.
3. Apply one medium-strength tap.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Data:

- Medium amplitude vibration
- Clear peak near the center of the recording

---

## Severe Fault

Purpose:

Simulate a strong mechanical impact.

Procedure:

1. Start recording.
2. Wait about 3–5 seconds.
3. Apply one strong impact.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Data:

- High vibration peak
- Maximum sensor response
- Returns to normal after the event

---

# Recording Guidelines

Each recording should satisfy the following conditions.

✅ Sensor fixed firmly

✅ One event per recording

✅ Event occurs near the middle of the recording

✅ Recording duration approximately 10–15 seconds

✅ No unnecessary movement

---

# File Naming Convention

Examples

```
normal_001.csv
normal_002.csv

minor_fault_001.csv

moderate_fault_001.csv

severe_fault_001.csv
```

---

# Dataset Verification Checklist

Before approving a dataset, verify the following:

- [x] Correct folder
- [x] Correct filename
- [x] CSV opens successfully
- [x] Header is correct
- [x] No empty rows
- [x] No missing values
- [x] Time values increase correctly
- [x] Event present in the recording
- [x] Event near the middle
- [x] Recording duration approximately 10–15 seconds

---

# Common Errors

❌ Sensor moved during Normal recording

❌ Multiple impacts in one recording

❌ Incorrect file name

❌ Empty CSV

❌ Missing header

❌ Missing samples

❌ Event occurs at the very beginning or end of the recording

---

# Team Member Responsibilities

Each contributor must:

- Follow the collection procedure.
- Verify every recording before uploading.
- Store files in the correct class folder.
- Follow the naming convention.
- Report corrupted or missing files.

---

# Version

Dataset Version: v1.0

Project: PhysiCore

Maintained by: Dataset Collection Team
