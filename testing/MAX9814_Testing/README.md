# MAX9814 Microphone Testing

## Project

**PhysiCore**  
AI-Based Intelligent Machine Fault Detection System

---

# Objective

This folder contains the Arduino testing code used to verify the functionality of the MAX9814 Electret Microphone Amplifier Module before collecting the machine sound dataset.

The purpose of this test is to ensure that the microphone is correctly connected, functioning properly, and producing valid analog output values.

---

# Hardware Used

| Component | Description |
|----------|-------------|
| Arduino Nano | Microcontroller |
| MAX9814 | Electret Microphone Amplifier |
| USB Cable | Power and Serial Communication |

---

# Hardware Connection

| MAX9814 | Arduino Nano |
|----------|--------------|
| VDD | 5V |
| GND | GND |
| OUT | A0 |
| GAIN | Leave Open |
| AR | Leave Open |

---

# Test Procedure

1. Connect the MAX9814 module according to the wiring table.
2. Upload the testing sketch.
3. Open the Arduino Serial Monitor.
4. Set the baud rate to **115200**.
5. Observe the microphone readings.
6. Produce different sounds near the microphone.
7. Verify that the sensor values change accordingly.

---

# Expected Behaviour

### Quiet Environment

The analog values should remain relatively stable.

Example

```
510
512
511
513
512
```

---

### Clap or Tap

The values should increase significantly.

Example

```
512
518
720
930
680
520
512
```

---

### Machine Sound

When the machine is operating, the values should continuously vary according to the sound intensity.

---

# Success Criteria

The sensor is considered functional if:

- [x] Arduino uploads successfully.
- [x] Serial Monitor displays analog values.
- [x] Values change when sound is present.
- [x] Values stabilize in a quiet environment.

---

# Troubleshooting

## Constant Value

Possible Causes

- Incorrect wiring
- OUT pin not connected
- Wrong analog pin
- Faulty sensor

---

## Always 0

Possible Causes

- No power
- Broken wire
- OUT connected incorrectly

---

## Random Noise

Possible Causes

- Loose jumper wires
- USB power noise
- Electrical interference

---

# Output Format

The Arduino sketch prints one analog value per line.

Example

```
512
513
511
515
820
950
610
520
```

---

# Arduino Sketch

The testing sketch continuously reads the microphone output using `analogRead()` and sends the values to the Serial Monitor.

---

# Folder Contents

```
MAX9814_Testing/
│
├── MAX9814_Testing.ino
├── README.md
```

---

# Notes

- This code is intended **only for hardware verification**.
- It is **not** used for dataset collection.
- Dataset collection uses a separate logging sketch that records timestamped sensor values into CSV files.

---

# Status

✅ Hardware Verification

Next Step:

➡ Collect machine sound dataset for AI model training.

---

Project: **PhysiCore**

Maintained by: Hardware Team
