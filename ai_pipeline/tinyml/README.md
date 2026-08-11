# TinyML Deployment

This directory contains the resources, implementation files, and documentation required to deploy the trained **PhysiCore machine-fault detection model** on an edge device.

---

## 🎯 Purpose

The purpose of the TinyML stage is to move the trained machine-fault detection system from a PC-based environment to a resource-constrained embedded device.

The final system should perform sensor processing, feature extraction, and fault classification locally on the edge device.

---

## 🔄 TinyML Pipeline

```text
Piezo Sensor
     │
     ▼
Data Acquisition
     │
     ▼
Preprocessing
     │
     ▼
Windowing
     │
     ▼
Feature Extraction
     │
     ▼
TinyML Model
     │
     ▼
Fault Classification
```

---

## 🤖 Current Model

The current baseline model is a **Random Forest classifier** trained using features extracted from the Piezo sensor.

### Model File

```text
ai_pipeline/models/piezo_random_forest.pkl
```

The current model is a PC-side machine-learning model and has not yet been converted for embedded deployment.

---

## 📊 Input Features

The model currently uses the following features extracted from each Piezo data window:

| Feature | Description |
|---|---|
| `Mean` | Mean value of the Piezo signal |
| `Std` | Standard deviation of the Piezo signal |
| `Variance` | Variance of the Piezo signal |
| `RMS` | Root Mean Square of the signal |
| `Maximum` | Maximum signal value |
| `Minimum` | Minimum signal value |
| `Peak_to_Peak` | Difference between maximum and minimum values |
| `Dominant_Frequency` | Dominant frequency obtained from FFT |
| `Spectral_Energy` | Energy calculated from the frequency-domain signal |

---

## 🏷️ Output Classes

The classifier identifies four machine-condition classes.

| Class ID | Condition |
|---:|---|
| `0` | Normal |
| `1` | Minor Fault |
| `2` | Moderate Fault |
| `3` | Severe Fault |

---

## 🔬 Complete AI Pipeline

```text
Raw Sensor Data
      │
      ▼
Preprocessing
      │
      ▼
Visualization
      │
      ▼
Windowing
      │
      ▼
Feature Engineering
      │
      ▼
Dataset Preparation
      │
      ▼
Train / Validation / Test Split
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
Inference
      │
      ▼
TinyML Deployment
```

---

## ⚙️ Target Embedded Pipeline

The final embedded system is intended to perform the following operations locally:

```text
Piezo Sensor
      │
      ▼
Sampling
      │
      ▼
Preprocessing
      │
      ▼
Windowing
      │
      ▼
Feature Extraction
      │
      ▼
TinyML Model
      │
      ▼
Prediction
      │
      ▼
Normal / Minor / Moderate / Severe
```

---

## 📥 Deployment Requirements

Before deployment, the following requirements must be evaluated:

- Model size
- RAM usage
- Flash/storage requirements
- Inference time
- Feature-extraction complexity
- Sensor sampling requirements
- Embedded processor capability
- Real-time prediction performance
- Memory requirements
- Power requirements
- Real-time processing capability

---

## 🔄 Model Conversion

The current model is stored as:

```text
piezo_random_forest.pkl
```

This model is intended for PC-based inference.

The `.pkl` model cannot be directly uploaded to a microcontroller as a TinyML model.

The deployment stage must therefore determine a suitable embedded representation or select a lightweight model architecture suitable for the target hardware.

The converted model must maintain the same input feature order and feature-calculation method used during training.

---

## 🔧 Hardware Deployment

The final TinyML implementation will operate on an embedded device connected to the Piezo sensor.

```text
┌─────────────────┐
│   Piezo Sensor  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Microcontroller │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preprocessing   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Feature         │
│ Extraction      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ TinyML Model    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fault Prediction│
└─────────────────┘
```

---

## 🧠 Real-Time Prediction

The final system should process new sensor data and produce a machine-condition prediction without requiring a PC.

Example:

```text
New Piezo Data
      │
      ▼
Preprocessing
      │
      ▼
Windowing
      │
      ▼
Feature Extraction
      │
      ▼
Model Inference
      │
      ▼
Prediction
      │
      ▼
Moderate Fault
```

---

## 🔁 Training vs Deployment

The processing performed during deployment must remain consistent with the processing used during model training.

```text
Training

Raw Data
   ↓
Preprocessing
   ↓
Windowing
   ↓
Feature Extraction
   ↓
Model Training
```

```text
Deployment

New Raw Data
   ↓
Same Preprocessing
   ↓
Same Windowing
   ↓
Same Feature Extraction
   ↓
Model Inference
```

Any difference between training-time and deployment-time processing can result in incorrect predictions.

---

## 📈 Model Performance

The trained model is evaluated using a separate test dataset that is not used during model training.

The evaluation stage measures:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix
- Per-class performance

The evaluation results are available in:

```text
ai_pipeline/evaluation/
```

---

## 📁 Directory Structure

```text
tinyml/
│
├── README.md
│
├── conversion/
│
├── embedded/
│
└── tests/
```

### Directory Description

| Directory | Purpose |
|---|---|
| `conversion/` | Model conversion and optimization files |
| `embedded/` | Embedded/TinyML implementation |
| `tests/` | Embedded deployment and hardware testing |

---

## 🚧 Current Status

| Stage | Status |
|---|---|
| Data Collection | ✅ Completed |
| Preprocessing | ✅ Completed |
| Visualization | ✅ Completed |
| Windowing | ✅ Completed |
| Feature Extraction | ✅ Completed |
| Dataset Preparation | ✅ Completed |
| Dataset Splitting | ✅ Completed |
| Model Training | ✅ Completed |
| Model Evaluation | ✅ Completed |
| PC Inference | ✅ Completed |
| TinyML Model Selection | ⏳ Pending |
| Model Conversion | ⏳ Pending |
| Model Optimization | ⏳ Pending |
| Embedded Implementation | ⏳ Pending |
| Hardware Testing | ⏳ Pending |
| Real-Time Fault Detection | ⏳ Pending |

---

## 🚀 Deployment Roadmap

```text
Trained Model
      │
      ▼
Model Analysis
      │
      ▼
Model Selection
      │
      ▼
Model Conversion
      │
      ▼
Model Optimization
      │
      ▼
Embedded Implementation
      │
      ▼
Hardware Testing
      │
      ▼
Real-Time Inference
      │
      ▼
Fault Detection System
```

---

## ⚠️ Important Notes

1. The TinyML model must use the same feature definitions used during training.

2. The order of input features must remain unchanged between training and deployment.

3. The preprocessing and windowing parameters must remain consistent.

4. The PC model should be validated before deployment to embedded hardware.

5. Memory usage and inference time must be checked before selecting the final embedded model.

6. The final embedded implementation must be tested using real sensor data.

---

## 🎯 Final Objective

The final TinyML system should be capable of receiving real-time Piezo sensor data and locally classifying the machine condition as:

```text
Normal
Minor Fault
Moderate Fault
Severe Fault
```

without requiring continuous PC-based machine-learning inference.
