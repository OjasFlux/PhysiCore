# MAX9814 Microphone Dataset Collection Guide

## Project

**PhysiCore**  
AI-Based Intelligent Machine Fault Detection System

---

# Objective

This dataset contains machine sound recordings collected using the MAX9814 Electret Microphone Amplifier Module.

The dataset will be used to train an AI model for detecting different machine operating conditions and fault levels based on acoustic signatures.

---

# Sensor Information

| Item | Details |
|------|---------|
| Sensor | MAX9814 Electret Microphone Amplifier |
| Sensor Type | Analog Audio Sensor |
| Microcontroller | Arduino Nano |
| Output | Analog (0–1023) |
| Sampling Interval | 20 ms |
| Sampling Rate | ~50 Hz |
| File Format | CSV |

---

# Hardware Connection

| MAX9814 | Arduino Nano |
|----------|--------------|
| VDD | 5V |
| GND | GND |
| OUT | A0 |
| GAIN | Leave Open |
| AR | Leave Open |

---

# Dataset Structure

```
dataset/
└── Microphone/
    ├── Normal/
    ├── Minor_Fault/
    ├── Moderate_Fault/
    └── Severe_Fault/
```

---

# CSV Format

Each CSV file contains two columns.

```csv
Time_ms,Microphone
0,512
20,514
40,515
60,720
80,910
100,520
```

---

# CSV Columns

| Column | Description |
|---------|-------------|
| Time_ms | Time elapsed from the beginning of the recording |
| Microphone | Raw analog microphone value (0–1023) |

---

# Data Collection Procedure

## Normal

### Purpose

Collect the normal operating sound of the machine without any abnormal events.

### Procedure

1. Place the microphone at a fixed distance from the machine.
2. Start recording.
3. Allow the machine to run normally.
4. Do not introduce any external noise or impacts.
5. Record for approximately 10–15 seconds.

Expected Result

- Stable background machine sound
- No abnormal spikes
- Consistent signal

---

## Minor Fault

### Purpose

Simulate a small abnormal machine sound.

### Procedure

1. Start recording.
2. Wait approximately 3–5 seconds.
3. Introduce one small mechanical sound (light knock, light crank, etc.).
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Result

- Small increase in microphone signal
- Event located near the middle of the recording

---

## Moderate Fault

### Purpose

Simulate a medium-level abnormal machine sound.

### Procedure

1. Start recording.
2. Wait approximately 3–5 seconds.
3. Produce one medium mechanical sound.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Result

- Medium-amplitude sound spike
- Returns to normal after the event

---

## Severe Fault

### Purpose

Simulate a strong abnormal machine sound.

### Procedure

1. Start recording.
2. Wait approximately 3–5 seconds.
3. Produce one strong mechanical sound.
4. Wait another 3–5 seconds.
5. Stop recording.

Expected Result

- High-amplitude sound spike
- Clear event near the center of the recording

---

# Recording Guidelines

Follow these rules for every recording.

✅ Keep the microphone position fixed.

✅ Maintain the same distance from the machine.

✅ Record only one event per recording.

✅ Event should occur near the middle of the recording.

✅ Recording duration should be approximately 10–15 seconds.

✅ Avoid talking or unnecessary background noise during recording.

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

Before approving any dataset, verify the following:
- [x] Correct folder
- [x] Correct filename
- [x] CSV opens correctly
- [x] Header is correct
- [x] No empty rows
- [x] No missing values
- [x] Time values increase correctly
- [x] Event occurs near the middle
- [x] Recording duration approximately 10–15 seconds
- [x] Microphone values change during the event

---

# Common Errors

❌ Microphone moved during recording

❌ Different microphone distance between recordings

❌ Multiple sound events in one recording

❌ Talking near the microphone

❌ Background noise (music, fans, conversations)

❌ Missing CSV header

❌ Empty or corrupted CSV file

---

# Team Member Responsibilities

Each contributor must:

- Follow the standard data collection procedure.
- Verify every recording before uploading.
- Keep the microphone in a fixed position.
- Use the correct naming convention.
- Upload files to the appropriate class folder.
- Report missing or corrupted recordings.

---

# Dataset Quality Requirements

| Requirement | Target |
|-------------|--------|
| Recording Duration | 10–15 seconds |
| Sampling Rate | ~50 Hz |
| Samples per Recording | ~500–750 |
| Events per Recording | One |
| Microphone Position | Fixed |
| Background Noise | Minimum |
| Missing Values | None |

---

# Notes

- Keep the microphone orientation and distance constant for all recordings.
- Use the same machine and operating conditions whenever possible.
- Ensure only the intended fault sound is introduced during each recording.

---

# Version

Dataset Version: v1.0

Project: PhysiCore

Maintained by: Dataset Collection Team
