# AI Pipeline

## Overview

This directory contains the complete Artificial Intelligence workflow for the PhysiCore project.

The pipeline transforms raw sensor data into a trained TinyML model capable of detecting machine operating conditions and mechanical faults.

---

# Pipeline Workflow

```
Raw Dataset
      │
      ▼
Data Preprocessing
      │
      ▼
Data Visualization
      │
      ▼
Feature Engineering
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
TinyML Conversion
      │
      ▼
Real-Time Inference
```

---

# Directory Structure

```
ai_pipeline/
├── preprocessing/
├── visualization/
├── feature_engineering/
├── training/
├── evaluation/
├── tinyml/
├── inference/
├── notebooks/
├── models/
└── README.md
```

---

# Pipeline Stages

| Stage | Description |
|--------|-------------|
| Preprocessing | Clean and prepare raw datasets |
| Visualization | Plot and inspect sensor data |
| Feature Engineering | Extract meaningful numerical features |
| Training | Train machine learning models |
| Evaluation | Evaluate model performance |
| TinyML | Convert model for embedded deployment |
| Inference | Real-time prediction on Arduino UNO Q |

---

# Sensors Used

- Piezo Sensor
- MPU6050
- MAX9814 Microphone

---

# Project

PhysiCore

AI-Based Intelligent Machine Fault Detection System
