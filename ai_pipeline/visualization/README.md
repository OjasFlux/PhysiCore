# Visualization

Contains scripts and outputs used to visually verify processed sensor signals.

## Purpose

Visualization checks signal presence, timestamp behavior, sensor variation, and possible differences between fault classes before ML processing.

## Piezo

```text
visualize_piezo.py
```

Classes:

- Normal
- Minor Fault
- Moderate Fault
- Severe Fault

## MPU6050

```text
visualize_mpu6050.py
```

Signals:

- Ax
- Ay
- Az
- Gx
- Gy
- Gz

## Status

- [x] Piezo visualization
- [x] MPU6050 visualization
- [ ] Microphone visualization

The microphone path is currently pending.
