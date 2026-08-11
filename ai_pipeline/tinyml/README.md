TINYML DEPLOYMENT

This directory contains the resources and implementation files required
to deploy the trained PhysiCore machine-fault detection model on an
edge device.


PURPOSE

The objective of the TinyML stage is to move the trained machine-fault
classification system from a PC-based environment to a resource-
constrained embedded device.


TINYML PIPELINE

Piezo Sensor
     |
     v
Data Acquisition
     |
     v
Preprocessing
     |
     v
Windowing
     |
     v
Feature Extraction
     |
     v
TinyML Model
     |
     v
Fault Classification


CURRENT MODEL

The current baseline model is a Random Forest classifier trained using
features extracted from the Piezo sensor.

Model:

ai_pipeline/models/piezo_random_forest.pkl

The current model is a PC-side model and has not yet been converted
for embedded deployment.


INPUT FEATURES

The model uses the following features:

1. Mean
2. Standard Deviation
3. Variance
4. RMS
5. Maximum
6. Minimum
7. Peak-to-Peak
8. Dominant Frequency
9. Spectral Energy


OUTPUT CLASSES

The classifier identifies four machine conditions:

0 - Normal
1 - Minor Fault
2 - Moderate Fault
3 - Severe Fault


COMPLETE AI PIPELINE

Raw Sensor Data
      |
      v
Preprocessing
      |
      v
Visualization
      |
      v
Windowing
      |
      v
Feature Engineering
      |
      v
Dataset Preparation
      |
      v
Train / Validation / Test Split
      |
      v
Model Training
      |
      v
Model Evaluation
      |
      v
Inference
      |
      v
TinyML Deployment


TARGET DEPLOYMENT PIPELINE

Piezo Sensor
      |
      v
Sampling
      |
      v
Preprocessing
      |
      v
Windowing
      |
      v
Feature Extraction
      |
      v
TinyML Model
      |
      v
Prediction
      |
      v
Normal / Minor / Moderate / Severe


DEPLOYMENT REQUIREMENTS

The following requirements must be evaluated before deployment:

- Model size
- RAM usage
- Flash/storage requirements
- Inference time
- Feature-extraction complexity
- Sensor sampling requirements
- Embedded processor capability
- Real-time prediction performance


MODEL CONVERSION

The current model:

piezo_random_forest.pkl

is intended for PC-based inference.

It cannot be directly uploaded to a microcontroller as a TinyML
model.

The deployment process must therefore determine a suitable embedded
representation or select a lightweight model architecture suitable
for the target hardware.


HARDWARE DEPLOYMENT

The final TinyML implementation will run on an embedded device
connected to the Piezo sensor.

Piezo Sensor
     |
     v
Microcontroller
     |
     v
Feature Extraction
     |
     v
TinyML Model
     |
     v
Fault Prediction


REAL-TIME PREDICTION

The final system should process new sensor windows and produce a
machine-condition prediction without requiring a PC.

Example:

New Piezo Window
      |
      v
Feature Extraction
      |
      v
Model Inference
      |
      v
Prediction: Moderate Fault


CURRENT STATUS

Data Collection              COMPLETED
Preprocessing                COMPLETED
Visualization                COMPLETED
Windowing                    COMPLETED
Feature Extraction           COMPLETED
Dataset Preparation           COMPLETED
Dataset Splitting             COMPLETED
Model Training                COMPLETED
Model Evaluation              COMPLETED
PC Inference                  COMPLETED
TinyML Model Selection        PENDING
Model Conversion              PENDING
Embedded Implementation       PENDING
Hardware Testing              PENDING
Real-Time Fault Detection     PENDING


IMPORTANT NOTE

The preprocessing, windowing, and feature-extraction operations used
during deployment must remain consistent with the operations used
during model training.

Any difference between training-time and deployment-time feature
calculations can result in incorrect model predictions.


DIRECTORY STRUCTURE

tinyml/
|
|-- README.md
|
|-- conversion/
|
|-- embedded/
|
`-- tests/


The subdirectories will contain model-conversion files, embedded
implementation files, and deployment-testing files as the TinyML
stage progresses.
