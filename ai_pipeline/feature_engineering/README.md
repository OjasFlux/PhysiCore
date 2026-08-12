# Feature Engineering

Converts fixed-size sensor windows into numerical features for machine learning.

## Workflow

```text
Windowed Sensor Data
    ↓
Time-Domain Features
    ↓
Frequency-Domain Features
    ↓
Feature Vector
    ↓
ML Dataset
```

## Piezo Features

- Mean
- Standard deviation
- Variance
- RMS
- Maximum
- Minimum
- Peak-to-Peak
- Dominant Frequency
- Spectral Energy

## Main Script

```text
extract_piezo_features.py
```

Output:

```text
piezo_features.csv
```

## Status

- [x] Piezo feature extraction
- [ ] MPU6050 feature extraction
- [ ] Microphone feature extraction

The microphone/INMP441 path is currently pending.
