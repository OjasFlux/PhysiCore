# MPU6050 Sensor Validation

## Objective

Verify that the MPU6050 accelerometer and gyroscope are functioning correctly with the Arduino UNO Q.

---

## Hardware

| Component | Quantity |
|-----------|---------:|
| Arduino UNO Q | 1 |
| MPU6050 Module | 1 |
| Jumper Wires | 4 |
| USB-C Cable | 1 |

---

## Wiring

| MPU6050 Pin | Arduino UNO Q |
|--------------|---------------|
| VCC | 3.3V |
| GND | GND |
| SDA | SDA |
| SCL | SCL |

---

## Interface

- Communication Protocol: **I²C**
- Supply Voltage: **3.3V**
- Sensor Type: 3-axis Accelerometer + 3-axis Gyroscope

---

## Software

- Arduino IDE 2.x
- Adafruit MPU6050 Library
- Adafruit Unified Sensor Library
- Adafruit BusIO Library

---

## Test Procedure

1. Connect the MPU6050 according to the wiring table.
2. Upload the MPU6050 test program.
3. Open the Serial Monitor.
4. Set the baud rate to **115200**.
5. Observe acceleration and gyroscope values.
6. Move and rotate the sensor in different directions.

---

## Expected Output

```
MPU6050 Connected!

Accel X: 0.10
Accel Y: -0.05
Accel Z: 9.80

Gyro X: 0.01
Gyro Y: -0.02
Gyro Z: 0.00
```

The values should change when the sensor is moved or rotated.

---

## Test Results

| Test | Result |
|------|--------|
| Device Detected | ☐ PASS / ☐ FAIL |
| Accelerometer Working | ☐ PASS / ☐ FAIL |
| Gyroscope Working | ☐ PASS / ☐ FAIL |
| Serial Communication | ☐ PASS / ☐ FAIL |

---

## Observations

- Sensor initialization completed successfully.
- Acceleration values responded to movement.
- Gyroscope values changed during rotation.
- Serial communication was stable.

---

## Conclusion

The MPU6050 sensor was successfully validated with the Arduino UNO Q and is ready for integration into the **PhysiCore** multimodal sensing platform.

---

## Future Work

- Sensor calibration
- Motion feature extraction
- Sensor fusion with Piezo and INMP441
- TinyML integration

---

**Project:** PhysiCore  
**Module:** MPU6050 Sensor Validation  
**Status:** Completed
