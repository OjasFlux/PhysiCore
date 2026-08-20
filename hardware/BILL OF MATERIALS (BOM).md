# Bill of Materials (BOM) - Edge AI Physical Interaction System

This project aims to develop an Edge AI system capable of understanding physical interactions using low-cost sensors, powered by an Arduino UNO Q.

## Core Hardware

| Component | Description | Quantity | Buying Links |
| :--- | :--- | :---: | :--- |
| **Arduino UNO Q** | Dual-brain AI development board with Linux & real-time control. | 1 | [Robu](https://robu.in/product/official-arduino-uno-q/) |
| **Piezo Vibration Sensor** | Sensor for detecting surface impacts, knocks, or physical vibrations. | 1 | [Techtonics](https://techtonics.in/product/piezo-vibration-sensor-large-with-mass/) / [Indian Hobby Center](https://www.indianhobbycenter.com/products/piezo-vibration-sensor) |
| **MPU6050 IMU** | 6-axis Motion Tracking device (Accelerometer + Gyroscope) for gesture/movement tracking. | 1 | [Robu](https://robu.in) / [CircuitDigest Shop](https://circuitdigest.com/shop) |

---

## Necessary Accessories (Recommended)
*Ensure you have these components on hand to complete the circuit:*

* **Breadboard:** For prototyping sensor connections.
* **Jumper Wires (Male-to-Male / Male-to-Female):** To hook up sensors to the Arduino headers.
* **USB-C Cable / Power Supply:** For programming and powering the Arduino UNO Q safely.

---

## Project Notes
* **Edge AI Constraint:** Since the system runs entirely on the Arduino UNO Q, configure your sensor sampling frequencies efficiently to fit within system memory constraints for any lightweight machine learning models (e.g., TinyML / TensorFlow Lite).
* **Communication Protocols:** The MPU6050 communicates via I2C, the MAX9814 provides analog output signals, and the Piezo sensor can be read via analog pins or digital interrupt pins depending on your trigger configuration.
