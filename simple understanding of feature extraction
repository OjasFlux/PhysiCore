# Feature Extraction

## Overview

Feature extraction is the process of converting raw sensor data into meaningful information that can be used by a Machine Learning (ML) or TinyML model. Instead of processing the complete raw signal, feature extraction identifies the most important characteristics of the data, reducing computational complexity and improving model performance.

In the **PhysiCore** project, feature extraction plays a vital role in analyzing data collected from the **INMP441 Microphone**, **Piezo Sensor**, and **MPU6050 Motion Sensor**. The extracted features help the TinyML model distinguish between normal and abnormal operating conditions.

---

# Why Feature Extraction?

Raw sensor signals contain a large amount of information, including useful patterns and unwanted noise. Processing raw signals directly requires more memory and processing power.

Feature extraction helps by:

- Reducing the amount of data to process
- Improving machine learning accuracy
- Reducing memory usage
- Enabling real-time processing
- Making TinyML models efficient on Arduino

---

# Selected Feature Extraction Techniques

The following feature extraction techniques were selected for the PhysiCore project:

- **Fast Fourier Transform (FFT)**
- **Root Mean Square (RMS)**
- **Signal Energy**
- **Zero Crossing Rate (ZCR)**

These techniques were chosen because they provide meaningful information while requiring minimal computational resources.

---

# Fast Fourier Transform (FFT)

## Description

Fast Fourier Transform (FFT) converts a signal from the **time domain** into the **frequency domain**. It identifies the frequency components present in sound and vibration signals.

## Why FFT?

Machine faults often produce changes in vibration and sound frequencies. FFT helps identify these frequency changes, making it useful for fault detection and machine monitoring.

### Advantages

- Detects frequency patterns
- Fast and accurate
- Suitable for sound and vibration analysis
- TinyML compatible

---

# Root Mean Square (RMS)

## Description

Root Mean Square (RMS) measures the overall strength or intensity of a signal.

## Why RMS?

Higher RMS values usually indicate stronger vibrations or louder sounds, which may represent abnormal machine conditions.

### Advantages

- Easy to calculate
- Low memory usage
- Fast processing
- Suitable for embedded systems

---

# Signal Energy

## Description

Signal Energy measures the total energy contained within a signal.

## Why Signal Energy?

Sudden impacts or machine faults usually increase the signal energy. This feature helps detect abnormal events quickly.

### Advantages

- Simple calculation
- Low computational cost
- Fast execution
- Suitable for TinyML

---

# Zero Crossing Rate (ZCR)

## Description

Zero Crossing Rate (ZCR) counts the number of times a signal crosses the zero-amplitude axis.

## Why ZCR?

Signals with higher frequencies cross the zero line more often. ZCR provides useful information about signal frequency changes.

### Advantages

- Very fast
- Easy to implement
- Low computational complexity
- Suitable for real-time applications

---

# Why These Features Were Selected

The PhysiCore platform uses three different sensors:

- 🎤 **INMP441 Microphone** – Captures sound signals
- 🔊 **Piezo Sensor** – Measures vibration
- 📈 **MPU6050 Motion Sensor** – Measures motion and acceleration

Each selected feature provides unique information:

| Feature | Purpose |
|---------|---------|
| FFT | Identifies frequency components |
| RMS | Measures signal strength |
| Signal Energy | Detects impacts and abnormal events |
| ZCR | Measures frequency changes |

Together, these features provide both time-domain and frequency-domain information while maintaining low computational complexity. This makes them ideal for TinyML deployment on Arduino.

---

# Conclusion

Feature extraction is an essential step in the PhysiCore project. After evaluating multiple techniques, **FFT**, **RMS**, **Signal Energy**, and **Zero Crossing Rate (ZCR)** were selected because they are lightweight, computationally efficient, and suitable for real-time TinyML applications.

These techniques improve machine learning performance while ensuring efficient execution on resource-constrained embedded systems such as Arduino.

---

# References

1. Pete Warden & Daniel Situnayake, *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*, O'Reilly Media, 2019.

2. TensorFlow Lite for Microcontrollers Documentation.

3. Randall, R.B., *Vibration-Based Condition Monitoring*, John Wiley & Sons.

4. IEEE Xplore Digital Library – Signal Processing and Feature Extraction.

5. Google TensorFlow Lite Documentation.
