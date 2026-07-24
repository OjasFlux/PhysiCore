# 📄 Research Paper 2

## Paper Title

**An Evaluation Methodology to Determine the Actual Limitations of a TinyML-Based Solution**

---

## Authors

- Giovanni Delnevo
- Silvia Mirri
- Catia Prandi
- Pietro Manzoni

---

## Publication Details

| Item | Details |
|------|---------|
| **Year** | 2023 |
| **Journal** | Internet of Things (Elsevier) |
| **DOI** | 10.1016/j.iot.2023.100729 |

---

# Abstract

This paper presents a methodology to evaluate how well TinyML models perform on low-power embedded devices. The researchers tested different machine learning algorithms on an Arduino Nano 33 BLE Sense to understand the practical limits of TinyML in real-world applications. 0

---

# Research Objective

The main objective of this research is to develop a standard methodology for evaluating TinyML applications running on embedded systems and to compare different machine learning algorithms for various sensing tasks. 1

---

# Problem Statement

Embedded devices such as Arduino have limited memory, processing power, and energy. It is important to understand which machine learning algorithms perform best under these constraints while maintaining good accuracy. 2

---

# Research Methodology

The researchers followed these steps:

1. Collect sensor data.
2. Prepare and label the dataset.
3. Train multiple machine learning models.
4. Test the models on an Arduino Nano 33 BLE Sense.
5. Compare model performance using evaluation metrics.

---

# Hardware Used

The experiments were performed using:

- Arduino Nano 33 BLE Sense

The board includes sensors such as:

- Microphone
- Accelerometer
- Gyroscope
- Color sensor

3

---

# Software Used

- Python
- TensorFlow
- Scikit-learn
- TensorFlow Lite
- EloquentTinyML Library

4

---

# Dataset

The researchers collected datasets for different tasks, including:

- Sound frequency recognition
- Vibration pattern recognition
- Vibration intensity detection
- Keyword spotting
- Hand gesture recognition
- Color recognition

5

---

# Machine Learning Models

The following models were evaluated:

- Random Forest
- Decision Tree
- Support Vector Classifier (SVC)
- Logistic Regression
- Gaussian Naive Bayes
- Multi-Layer Perceptron (MLP)

6

---

# Feature Extraction

The study focused on extracting useful information from sensor signals for classification tasks, including:

- Sound frequency information
- Vibration patterns
- Sensor measurements

These extracted features were then used to train machine learning models. 7

---

# Performance Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Memory Usage
- Inference Time

8

---

# Advantages

- Provides a complete TinyML evaluation methodology.
- Compares multiple machine learning algorithms.
- Demonstrates real-time execution on Arduino.
- Evaluates memory and processing limitations.

---

# Limitations

- Uses limited datasets collected in laboratory conditions.
- Performance depends on the hardware capabilities.
- Complex models require more memory and processing power.

---

# Why This Paper is Useful for PhysiCore

This paper is highly relevant to the PhysiCore project because it demonstrates how TinyML models can be evaluated on Arduino hardware. It also shows how sound and vibration data can be collected, processed, and classified efficiently on embedded systems.

The methodology can be adapted for PhysiCore to evaluate TinyML models using features such as **FFT**, **RMS**, **Signal Energy**, and **Zero Crossing Rate (ZCR)**.

---

# Key Findings

- TinyML can successfully run on Arduino-class devices.
- Random Forest, Decision Tree, and Support Vector Classifier achieved strong performance in several sensing tasks.
- Performance should be evaluated using both accuracy and hardware resource usage.

---

# Conclusion

The paper concludes that TinyML is practical for embedded applications when lightweight models and efficient feature extraction methods are used. A structured evaluation methodology helps developers choose the most suitable algorithm for their application. 9

---

# Reference

Delnevo, G., Mirri, S., Prandi, C., & Manzoni, P. (2023). **An Evaluation Methodology to Determine the Actual Limitations of a TinyML-Based Solution.** *Internet of Things*, Volume 22, Article 100729. https://doi.org/10.1016/j.iot.2023.100729 10
````11
