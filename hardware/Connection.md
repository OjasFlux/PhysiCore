# Hardware Connections

This document describes the hardware connections used in the **PhysiCore** project.

## Hardware Components

| Component | Interface | Purpose |
|----------|-----------|---------|
| Arduino UNO Q | Main Controller | Edge AI Processing |
| IMAX9814 | Analog | Audio Acquisition |
| Piezo Sensor | Analog | Vibration Detection |
| MPU6050 | I2C | Motion Sensing |
| Status LEDs | GPIO | System Status |

---

# System Architecture

```
                Physical Object
                      │
                 Tap / Impact
                      │
      ┌──────────┬───────────┬───────────┐
      │          │           │
  INMP441     Piezo      MPU6050
 (Audio)   (Vibration)   (Motion)
      │          │           │
      └──────────┼───────────┘
                 │
          Arduino UNO Q
                 │
      Signal Processing & TinyML
                 │
       Material Classification
```

---

# Connection Table

## INMP441 Digital Microphone

| INMP441 Pin | Arduino UNO Q |
|-------------|---------------|
| VDD | 3.3V |
| GND | GND |
| WS | I2S Word Select |
| SCK | I2S Bit Clock |
| SD | I2S Data |
| L/R | GND (Left Channel) |

---

## Piezo Sensor

| Piezo Pin | Arduino UNO Q |
|------------|--------------|
| Signal | A0 |
| GND | GND |

### Recommended Circuit

```
Piezo
  │
  ├────── A0
  │
1 MΩ
  │
 GND
```

---

## MPU6050

| MPU6050 Pin | Arduino UNO Q |
|--------------|---------------|
| VCC | 3.3V |
| GND | GND |
| SDA | SDA |
| SCL | SCL |

---

## Status LEDs

| LED | Arduino Pin |
|-----|-------------|
| Green LED | D8 |
| Red LED | D9 |

Use a **220 Ω resistor** in series with each LED.

---

# Power Supply

| Device | Supply Voltage |
|----------|---------------|
| Arduino UNO Q | USB-C |
| INMP441 | 3.3V |
| MPU6050 | 3.3V |
| Piezo | Passive Sensor |

---

# Communication Interfaces

| Interface | Device |
|-----------|--------|
| I2S | INMP441 |
| I2C | MPU6050 |
| Analog ADC | Piezo Sensor |
| GPIO | LEDs |

---

# Notes

- Ensure all sensors share a common GND.
- Use the official Arduino UNO Q pinout before final hardware assembly.
- Keep microphone wires short to reduce electrical noise.
- Mount the piezo sensor firmly for consistent vibration measurements.
- Verify all connections before powering the board.

---

# Future Expansion

The hardware architecture supports additional sensors such as:

- Temperature Sensor
- Force Sensor
- Load Cell
- Ultrasonic Sensor
- Environmental Sensors

without significant modifications to the system architecture.

---

**Project:** PhysiCore  
**Platform:** Arduino UNO Q  
**Version:** 1.0
