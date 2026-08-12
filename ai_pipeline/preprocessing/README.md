# Preprocessing

Contains preprocessing and windowing scripts for preparing raw sensor recordings.

## Preprocessing

```text
Raw Data
  ↓
Read CSV
  ↓
Remove Missing Rows
  ↓
Remove Duplicates
  ↓
Reset Timestamp
  ↓
Processed Data
```

## Windowing

Current baseline:

```text
Window Size : 100 samples
Step Size   : 50 samples
```

## Piezo

Scripts:

```text
preprocess_piezo.py
window_piezo.py
```

Current windowing result:

```text
Files processed : 120
Total windows   : 1566
```

## MPU6050

Scripts:

```text
preprocess_mpu6050.py
window_mpu6050.py
```

Current result:

```text
Files processed : 120
Failed files    : 0
Total windows   : 501
```

## Microphone

MAX9814 collection is currently paused. The INMP441 + ESP32 + UNO Q hardware communication path has been verified, but the microphone dataset pipeline is pending.

## Important

Do not remove valid sensor zero readings unless a verified data-quality rule requires it.
