# 📄 Research Paper 3

## Paper Title

**A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era**

---

## Authors

- Francisco Gómez
- Pablo A. Tarifa
- Diego G. Rodríguez
- and other researchers

---

## Publication Details

| Item | Details |
|------|---------|
| **Year** | 2026 |
| **Journal** | Sensors (MDPI) |
| **Research Area** | TinyML, Predictive Maintenance, Industrial IoT, Edge AI |

---

# Abstract

This paper presents a TinyML-based predictive maintenance system that monitors industrial machines using multiple sensors. The system performs machine learning directly on embedded devices, reducing latency and improving real-time fault detection.

---

# Research Objective

The main objective is to develop a lightweight TinyML system that can detect machine faults using multiple sensor types while running efficiently on embedded hardware.

---

# Problem Statement

Traditional predictive maintenance systems often rely on cloud computing, which increases latency and network dependency.

This research proposes an edge-based TinyML solution that performs data processing and fault detection directly on embedded devices.

---

# Research Methodology

The researchers followed these steps:

1. Collect machine data using multiple sensors.
2. Extract important features from vibration and acoustic signals.
3. Train TinyML models.
4. Deploy the models on embedded hardware.
5. Evaluate performance using real industrial data.

---

# Hardware Used

The system uses:

- Arduino Portenta H7
- Arduino Nicla Sense ME
- Arduino Nicla Voice
- MEMS Accelerometer
- MEMS Microphone
- Thermal Camera

---

# Software Used

- Arduino IDE
- Edge Impulse
- TensorFlow Lite for Microcontrollers
- AWS IoT

---

# Sensors Used

- Vibration Sensor (MEMS Accelerometer)
- Acoustic Sensor (Microphone)
- Thermal Camera

---

# Feature Extraction Techniques Used

The paper uses different feature extraction methods for different sensing modalities.

### Vibration

The vibration model extracts **10 time-domain statistical features** from vibration signals before TinyML inference.

### Acoustic

The acoustic model extracts **log-Mel filterbank (log-Mel) features**, which are well suited for audio analysis.

### Thermal

Thermal images are processed using a lightweight CNN instead of handcrafted features.

---

# Machine Learning Models

The research evaluates:

- Quantized Autoencoder
- Logistic Regression
- Convolutional Neural Network (CNN)

The quantized autoencoder achieved the best performance for vibration anomaly detection.

---

# Performance Evaluation

The system was evaluated using:

- Accuracy
- F1-Score
- Inference Latency
- Flash Memory Usage

The best model achieved an **F1-score of approximately 0.98** while requiring only a small Flash footprint and very low inference latency.

---

# Advantages

- Real-time monitoring
- Low latency
- Low power consumption
- Suitable for TinyML
- Supports multiple sensors
- Edge-based processing

---

# Limitations

- Requires multiple sensors
- Acoustic processing is more computationally demanding than vibration processing
- Tested on a controlled industrial setup

---

# Why This Paper is Useful for PhysiCore

This paper is highly relevant because PhysiCore also combines multiple sensors and TinyML.

It demonstrates how embedded devices can process vibration and acoustic signals locally, reducing latency and cloud dependency.

The paper also provides a practical example of selecting lightweight feature extraction methods based on the sensor type.

---

# Key Findings

- TinyML can perform predictive maintenance directly on embedded devices.
- Multiple sensing modalities improve fault detection.
- Lightweight feature extraction enables real-time processing.
- Embedded AI reduces communication overhead and power consumption.

---

# Conclusion

The paper concludes that TinyML-based predictive maintenance is practical for Industrial IoT applications. By combining lightweight feature extraction with embedded machine learning, accurate fault detection can be achieved while operating within the memory and processing limits of microcontrollers.

---

# Reference

**Gómez, F., et al.** *A Multimodal TinyML-Based Predictive Maintenance Architecture for Industrial IoT in the 6G Era.* Sensors, 2026.
