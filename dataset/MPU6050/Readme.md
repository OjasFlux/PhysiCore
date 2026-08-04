# MPU6050 Sensor Dataset Collection Guide

## Project

**PhysiCore**
AI-Based Intelligent Machine Fault Detection System

---

# Objective

This dataset contains motion and vibration data collected using the MPU6050 (3-Axis Accelerometer + 3-Axis Gyroscope).

The dataset will be used to train an AI model capable of recognizing machine operating conditions and fault levels.

---

# Sensor Information

| Item | Details |
|------|---------|
| Sensor | MPU6050 |
| Type | 3-Axis Accelerometer + 3-Axis Gyroscope |
| Microcontroller | Arduino Nano |
| Communication | I2C |
| Sampling Interval | 20 ms |
| Sampling Rate | ~50 Hz |
| Output | Ax, Ay, Az, Gx, Gy, Gz |
| File Format | CSV |

---

# Hardware Connection

| MPU6050 | Arduino Nano |
|----------|--------------|
| VCC | 3.3V-5V |
| GND | GND |
| SDA | A4 |
| SCL | A5 |

---

# Dataset Structure

```
dataset/
└── MPU6050/
    ├── Normal/
    ├── Minor_Fault/
    ├── Moderate_Fault/
    └── Severe_Fault/
```

---

# CSV Format

Each CSV contains seven columns.

```csv
Time_ms,Ax,Ay,Az,Gx,Gy,Gz
0,8.42,0.15,-5.61,-0.02,0.01,-0.03
20,8.43,0.16,-5.60,-0.03,0.01,-0.02
40,8.41,0.15,-5.61,-0.02,0.00,-0.01
```

---

# CSV Columns

| Column | Description |
|---------|-------------|
| Time_ms | Time elapsed from the start of recording |
| Ax | Acceleration along X-axis (m/s²) |
| Ay | Acceleration along Y-axis (m/s²) |
| Az | Acceleration along Z-axis (m/s²) |
| Gx | Angular velocity around X-axis (rad/s) |
| Gy | Angular velocity around Y-axis (rad/s) |
| Gz | Angular velocity around Z-axis (rad/s) |

---

# Data Collection Procedure

## Normal

### Purpose

Collect normal machine vibration without any external disturbance.

### Procedure

1. Mount the MPU6050 securely.
2. Start recording.
3. Do not move or touch the sensor.
4. Record for approximately 10–15 seconds.
5. Save the CSV file.

Expected Result

- Stable acceleration values
- Stable gyroscope values
- Only small sensor noise

---

## Minor Fault

### Purpose

Simulate a small vibration or light machine fault.

### Procedure

1. Start recording.
2. Wait approximately 3–5 seconds.
3. Apply one light tap or small vibration.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Result

- Small change in acceleration
- Small change in gyroscope values
- Returns to normal after the event

---

## Moderate Fault

### Purpose

Simulate a moderate mechanical fault.

### Procedure

1. Start recording.
2. Wait approximately 3–5 seconds.
3. Apply one medium-strength impact.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Result

- Medium acceleration peak
- Medium angular velocity peak
- Event located near the center of the recording

---

## Severe Fault

### Purpose

Simulate a severe machine fault.

### Procedure

1. Start recording.
2. Wait approximately 3–5 seconds.
3. Apply one strong impact.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Result

- High acceleration peak
- High gyroscope response
- Returns to normal after the event

---

# Recording Guidelines

Follow these rules for every recording.

✅ Fix the MPU6050 securely.

✅ Keep the sensor orientation unchanged.

✅ Record only one event per CSV.

✅ Event should occur near the middle of the recording.

✅ Recording duration should be approximately 10–15 seconds.

✅ Avoid unnecessary movement during recording.

---

# File Naming Convention

Examples

```
normal_001.csv
normal_002.csv
normal_003.csv

minor_fault_001.csv
minor_fault_002.csv

moderate_fault_001.csv

severe_fault_001.csv
```

---

# Dataset Verification Checklist

Before approving any dataset, verify the following:

- [ x] Correct folder
- [x ] Correct filename
- [ x] CSV file opens correctly
- [x ] Header is correct
- [x ] Seven columns are present
- [x] No empty rows
- [ x] No missing values
- [ x] Time values increase correctly
- [ x] Sensor orientation remained unchanged
- [x] Event occurs near the middle
- [ ] Recording duration approximately 10–15 seconds

---

# Common Errors

❌ Holding the sensor by hand during recording

❌ Changing sensor orientation between recordings

❌ Multiple impacts in a single recording

❌ Missing CSV header

❌ Empty rows

❌ Corrupted CSV file

❌ Event occurs at the beginning or end of the recording

---

# Team Member Responsibilities

Each contributor must:

- Follow the standard data collection procedure.
- Verify every CSV before uploading.
- Upload files to the correct class folder.
- Follow the naming convention.
- Report corrupted or incomplete datasets.
- Keep the sensor orientation consistent throughout the collection process.

---

# Dataset Quality Requirements

| Requirement | Target |
|-------------|--------|
| Recording Duration | 10–15 seconds |
| Sampling Rate | ~50 Hz |
| Samples per Recording | ~500–750 |
| Events per Recording | One |
| Sensor Orientation | Fixed |
| Missing Values | None |

---

# Version

Dataset Version: v1.0

Project: PhysiCore

Maintained by: Dataset Collection Team
