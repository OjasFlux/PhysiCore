# 📄 Research Paper 4

## Paper Title

**IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML**

---

## Authors

- Stalin Arciniegas
- Dulce Rivero
- Jefferson Piñan
- Elizabeth Diaz
- Francklin Rivas

---

## Year

**2025**

---

## Journal

**Discover Internet of Things (Springer Nature)**

---

# Objective

The main objective of this paper is to detect abnormal motor vibrations using **TinyML** on an embedded device. The system can identify machine faults quickly without using cloud computing.

---

# Problem Statement

Traditional machine monitoring systems require:

- High processing power
- Cloud connection
- More time for processing

These systems are expensive and slow for real-time monitoring.

The proposed TinyML system solves this problem by processing vibration data directly on the embedded device.

---

# Methodology

The researchers followed these steps:

1. Collect vibration data from the motor.
2. Remove unwanted noise from the signal.
3. Extract important features from the vibration signal.
4. Train the TinyML model.
5. Deploy the trained model on the embedded device.
6. Detect abnormal motor vibrations in real time.

---

# Hardware Used

- Embedded IoT Device
- Vibration Sensor (Accelerometer)
- Electric Motor

---

# Software Used

- Arduino IDE
- TensorFlow Lite
- Edge Impulse

---

# Feature Extraction

The researchers used **frequency-based feature extraction** to analyze the vibration signals.

The extracted features help the TinyML model identify whether the motor is operating normally or has a fault.

---

# Machine Learning Model

The paper uses a lightweight TinyML model that can run efficiently on embedded hardware.

---

# Results

- High fault detection accuracy
- Fast processing
- Real-time monitoring
- Low memory usage
- Low power consumption

---

# Advantages

- Fast fault detection
- Low power consumption
- Real-time monitoring
- Suitable for embedded systems
- Easy to deploy on TinyML devices

---

# Limitations

- Tested using a limited motor dataset.
- Performance may change for different types of motors.

---

# Why This Paper is Useful for PhysiCore

This paper is useful because it explains how TinyML can detect machine faults using vibration data.

The approach is similar to the PhysiCore project, where sensor data is processed on an embedded device for real-time monitoring.

---

# Conclusion

This paper shows that TinyML can successfully detect abnormal motor vibrations on embedded devices.

Using lightweight feature extraction and TinyML makes the system fast, efficient, and suitable for real-time applications.

---

# Reference

Arciniegas, S., Rivero, D., Piñan, J., Diaz, E., & Rivas, F. (2025).

**IoT Device for Detecting Abnormal Vibrations in Motors Using TinyML.**

*Discover Internet of Things*, Springer Nature.
