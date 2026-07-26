# 📄 Research Paper 5

## Paper Title

**Edge-Based TinyML for Fault Detection Using Sound Vibration Analysis**

---

## Authors

Multiple Authors

---

## Year

**2025**

---

## Conference

**2025 Second International Conference on Intelligent Technologies for Sustainable Electric and Communications Systems (IEEE)**

---

# Objective

The objective of this research is to detect machine faults using **sound and vibration signals** by deploying a **TinyML model** directly on an embedded device. This enables fast and accurate fault detection without relying on cloud computing. 0

---

# Problem Statement

Traditional fault detection systems send sensor data to cloud servers for processing. This causes:

- Higher latency
- More power consumption
- Internet dependency
- Privacy concerns

The proposed system processes the data locally using TinyML to overcome these problems. 1

---

# Methodology

The researchers followed these steps:

1. Collect sound and vibration data from industrial machines.
2. Preprocess the collected signals.
3. Extract useful features from the signals.
4. Train a lightweight TinyML model.
5. Deploy the model on an Arduino Nano RP2040.
6. Detect machine faults in real time. 2

---

# Hardware Used

- Arduino Nano RP2040
- Microphone
- Vibration Sensor

---

# Software Used

- TensorFlow Lite for Microcontrollers
- Arduino IDE

---

# Feature Extraction

The researchers used:

- **Mel Frequency Energy (MFE)**

MFE extracts important frequency information from sound signals before classification. It provides a compact representation of acoustic features suitable for TinyML models. 3

---

# Machine Learning Model

The system uses a lightweight TinyML neural network optimized for embedded devices.

---

# Results

- Fast fault detection
- Low latency
- Low power consumption
- Real-time processing
- Improved privacy because data is processed on the device instead of the cloud. 4

---

# Advantages

- Real-time monitoring
- Fast processing
- Low energy consumption
- No cloud dependency
- Suitable for embedded systems

---

# Limitations

- Tested on industrial sound datasets.
- Performance depends on the quality of the collected sensor data.

---

# Why This Paper is Useful for PhysiCore

This paper is closely related to the PhysiCore project because it uses:

- TinyML
- Arduino-based hardware
- Sound analysis
- Vibration monitoring
- Edge AI

Although the paper uses **Mel Frequency Energy (MFE)** instead of FFT, RMS, Signal Energy, or ZCR, it demonstrates how lightweight audio features can be extracted and processed directly on embedded hardware for real-time machine fault detection.

---

# Conclusion

The paper concludes that TinyML enables accurate and efficient machine fault detection directly on embedded devices. Processing data locally reduces latency, lowers power consumption, and eliminates the need for continuous cloud connectivity. 5

---

# Reference

**Edge-Based TinyML for Fault Detection Using Sound Vibration Analysis**, Proceedings of the **2025 Second International Conference on Intelligent Technologies for Sustainable Electric and Communications Systems (IEEE)**.
