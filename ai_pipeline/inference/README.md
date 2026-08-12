# Inference

Runs trained models on new, unseen sensor data.

## Workflow

```text
New Sensor Data
    ↓
Preprocessing
    ↓
Windowing
    ↓
Feature Extraction
    ↓
Trained Model
    ↓
Fault Prediction
```

## Piezo

Main script:

```text
predict_piezo.py
```

Model:

```text
ai_pipeline/models/piezo_random_forest.pkl
```

## Output Classes

| ID | Condition |
|---:|---|
| 0 | Normal |
| 1 | Minor Fault |
| 2 | Moderate Fault |
| 3 | Severe Fault |

## Status

- [x] PC inference implemented
- [x] Piezo prediction
- [ ] Multi-sensor inference
- [ ] Real-time inference
- [ ] Embedded inference
