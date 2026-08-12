# TinyML Deployment

Contains model analysis, conversion, embedded implementation, and testing resources for edge deployment.

## Pipeline

```text
Piezo Sensor
    ↓
Sampling
    ↓
Preprocessing
    ↓
Windowing
    ↓
Feature Extraction
    ↓
TinyML Model
    ↓
Fault Classification
```

## Selected Candidate

```text
ai_pipeline/models/piezo_decision_tree.pkl
```

Characteristics:

```text
Tree depth : 4
Leaves     : 6
Test accuracy : 99.57%
```

## Converted Model

```text
ai_pipeline/tinyml/conversion/piezo_decision_tree.h
```

Conversion verification passed and the generated tree logic matches the scikit-learn model.

## Features

- Mean
- Std
- Variance
- RMS
- Maximum
- Minimum
- Peak_to_Peak
- Dominant_Frequency
- Spectral_Energy

## Classes

| ID | Condition |
|---:|---|
| 0 | Normal |
| 1 | Minor Fault |
| 2 | Moderate Fault |
| 3 | Severe Fault |

## Status

- [x] TinyML candidate selected
- [x] Decision Tree trained
- [x] Decision Tree evaluated
- [x] Model converted to C/C++
- [x] Conversion verified
- [ ] Embedded feature extraction
- [ ] Embedded inference
- [ ] Hardware testing
- [ ] Real-time fault detection

## Structure

```text
tinyml/
├── README.md
├── conversion/
├── embedded/
└── tests/
```
