# Training Pipeline

Contains dataset preparation, dataset splitting, and model-training resources.

## Workflow

```text
Feature Dataset
    ↓
Dataset Preparation
    ↓
Train / Validation / Test Split
    ↓
Model Training
    ↓
Validation
```

## Dataset Preparation

Script:

```text
prepare_piezo_dataset.py
```

Label mapping:

| Class | ID |
|---|---:|
| Normal | 0 |
| Minor_Fault | 1 |
| Moderate_Fault | 2 |
| Severe_Fault | 3 |

## Dataset Split

Script:

```text
split_piezo_dataset.py
```

Current split:

```text
Training   : 70%
Validation : 15%
Testing    : 15%
```

Output:

```text
dataset_split/
├── X_train.csv
├── X_validation.csv
├── X_test.csv
├── y_train.csv
├── y_validation.csv
└── y_test.csv
```

## Status

- [x] Feature dataset prepared
- [x] Labels encoded
- [x] Train/validation/test split
- [x] Random Forest training
- [x] Decision Tree training
- [x] Validation
- [x] Test dataset prepared
