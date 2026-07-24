# Feature Extraction Techniques for PhysiCore

## Project
**PhysiCore: A Self-Learning Physical Intelligence Platform for Edge AI on Arduino**

---

# Overview

Feature extraction is the process of converting raw sensor signals into meaningful numerical values that can be used by machine learning models. Instead of processing raw sensor data directly, extracted features reduce computational complexity, improve model accuracy, and enable efficient execution on embedded systems.

For the PhysiCore platform, the following feature extraction techniques are selected:

- Fast Fourier Transform (FFT)
- Root Mean Square (RMS)
- Signal Energy
- Zero Crossing Rate (ZCR)

These techniques are lightweight, computationally efficient, and suitable for TinyML deployment on Arduino.

---

# Table of Contents

1. Fast Fourier Transform (FFT)
2. Root Mean Square (RMS)
3. Signal Energy
4. Zero Crossing Rate (ZCR)
5. Feature Comparison
6. Why These Features?
7. Conclusion

---

# 1. Fast Fourier Transform (FFT)

## Definition

Fast Fourier Transform (FFT) is an efficient algorithm used to convert a signal from the **time domain** into the **frequency domain**.

Instead of showing how a signal changes over time, FFT reveals the frequencies that make up the signal and their corresponding amplitudes.

---

## Why FFT?

Mechanical faults often create unique frequency patterns. FFT helps identify these patterns by analyzing vibration and sound signals.

---

## Working Principle

```
Time Domain Signal

Amplitude
│
│      /\      /\      /\
│     /  \    /  \    /  \
└──────────────────────────► Time

              FFT

Frequency Domain

Amplitude
│
│         █
│      █████
│   █████████
└──────────────────────────► Frequency
```

---

## Mathematical Formula

The Discrete Fourier Transform (DFT) is

```
            N−1
X(k) = Σ x(n)e^(−j2πkn/N)
            n=0
```

FFT is a faster algorithm for computing the DFT.

---

## Applications

- Machine vibration analysis
- Bearing fault detection
- Motor health monitoring
- Acoustic signal analysis
- Structural health monitoring

---

## Advantages

- Fast frequency analysis
- High accuracy
- Suitable for embedded systems
- Works well with TinyML

---

## Limitations

- Requires more computation than RMS or ZCR
- Requires windowing for best performance

---

## Computational Complexity

```
O(N log N)
```

---

## Output

FFT produces:

- Dominant frequency
- Frequency spectrum
- Harmonic components

---

# 2. Root Mean Square (RMS)

## Definition

Root Mean Square (RMS) measures the effective magnitude or strength of a signal.

It provides an estimate of the average signal power.

---

## Mathematical Formula

```
          ______________________
         / Σ(x²)
RMS = √  ----------
              N
```

---

## Why RMS?

Higher vibration levels usually indicate abnormal machine conditions.

Example:

| Machine State | RMS Value |
|---------------|-----------|
| Normal | 0.18 |
| Faulty | 0.72 |

---

## Applications

- Machine health monitoring
- Vibration analysis
- Sound intensity measurement
- Impact detection

---

## Advantages

- Very easy to compute
- Low memory usage
- Noise resistant
- Excellent for TinyML

---

## Limitations

- Does not provide frequency information

---

## Computational Complexity

```
O(N)
```

---

## Output

Example

```
RMS = 0.45
```

---

# 3. Signal Energy

## Definition

Signal Energy represents the total energy contained in a signal.

It indicates the amount of activity or impact present within the measured signal.

---

## Mathematical Formula

```
Energy = Σ(x²)
```

---

## Why Signal Energy?

A damaged machine generally produces stronger vibrations, resulting in higher energy values.

Example:

| Machine State | Energy |
|---------------|---------|
| Normal | 120 |
| Impact Detected | 2450 |

---

## Applications

- Fault diagnosis
- Event detection
- Machine monitoring
- Impact detection

---

## Advantages

- Extremely simple
- Very fast
- Low memory usage
- Suitable for TinyML

---

## Limitations

- Does not indicate frequency content

---

## Computational Complexity

```
O(N)
```

---

## Output

```
Energy = 1832
```

---

# 4. Zero Crossing Rate (ZCR)

## Definition

Zero Crossing Rate (ZCR) measures how many times a signal crosses the zero-amplitude axis during a given time interval.

---

## Mathematical Formula

```
              1
ZCR = --------------- Σ |sign(xi)-sign(xi−1)|
          2N
```

---

## Why ZCR?

Higher frequency signals cross zero more frequently.

Example:

| Signal Type | Zero Crossings |
|-------------|----------------|
| Low Frequency | 18 |
| High Frequency | 135 |

---

## Applications

- Speech detection
- Audio classification
- Noise detection
- Vibration analysis

---

## Advantages

- Extremely fast
- Very low computational cost
- Easy implementation
- Excellent for TinyML

---

## Limitations

- Sensitive to noise
- Does not measure signal amplitude

---

## Computational Complexity

```
O(N)
```

---

## Output

```
ZCR = 96
```

---

# Feature Comparison

| Feature | Output | Complexity | TinyML Compatible | Primary Purpose |
|----------|--------|------------|-------------------|-----------------|
| FFT | Frequency Spectrum | O(N log N) | Yes | Frequency Analysis |
| RMS | Signal Magnitude | O(N) | Yes | Measure Signal Strength |
| Signal Energy | Total Energy | O(N) | Yes | Detect Impacts |
| ZCR | Zero Crossing Count | O(N) | Yes | Estimate Frequency Changes |

---

# Why These Features?

The PhysiCore platform uses multiple sensors:

- 🎤 INMP441 Microphone (Sound)
- 🔊 Piezo Sensor (Vibration)
- 📈 MPU6050 (Motion)

The selected features complement each other:

- **FFT** identifies frequency components in sound and vibration.
- **RMS** measures signal intensity.
- **Signal Energy** detects impacts and abnormal events.
- **Zero Crossing Rate** estimates rapid frequency changes.

Together, these features provide meaningful information while maintaining low computational complexity, making them ideal for TinyML deployment on Arduino.

---

# Conclusion

FFT, RMS, Signal Energy, and Zero Crossing Rate (ZCR) form an efficient feature extraction pipeline for the PhysiCore platform. They improve machine learning performance by transforming raw sensor signals into meaningful numerical features while requiring minimal computational resources.

These techniques are highly suitable for TinyML-based embedded AI systems because they offer a balance between accuracy, speed, and memory efficiency.

---

# References

1. Pete Warden & Daniel Situnayake, *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*, O'Reilly Media, 2019.

2. TensorFlow Lite for Microcontrollers Documentation.

3. IEEE Xplore Digital Library – Signal Processing and Feature Extraction.

4. Randall, R.B., *Vibration-Based Condition Monitoring*, John Wiley & Sons.

5. Google TensorFlow Lite Official Documentation.
