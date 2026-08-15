#include <Wire.h>
#include <math.h>
#include "mpu6050_decision_tree.h"

// =====================================================
// PhysiCore - MPU6050 TinyML
// Target: Arduino UNO Q
//
// IMPORTANT:
// The sampling/window settings and sensor scaling must
// match the data used to train the Python model.
// =====================================================

// =====================================================
// MPU6050
// =====================================================

#define MPU6050_ADDR 0x68

// MPU6050 registers
#define PWR_MGMT_1   0x6B
#define ACCEL_XOUT_H 0x3B
#define GYRO_XOUT_H  0x43

// =====================================================
// WINDOW
// =====================================================

// Must match the MPU6050 window size used during training.
const int WINDOW_SIZE = 100;

// Change this if your actual MPU6050 training window used
// a different number of samples.
const unsigned long SAMPLE_INTERVAL_US = 20000;

// 50 Hz
const float SAMPLE_RATE = 50.0;

// =====================================================
// FEATURE COUNT
// =====================================================

const int FEATURE_COUNT = 56;

// =====================================================
// RAW SENSOR WINDOWS
// =====================================================

float ax[WINDOW_SIZE];
float ay[WINDOW_SIZE];
float az[WINDOW_SIZE];

float gx[WINDOW_SIZE];
float gy[WINDOW_SIZE];
float gz[WINDOW_SIZE];

// =====================================================
// FEATURE VECTOR
//
// Order:
// 0-6   Ax
// 7-13  Ay
// 14-20 Az
// 21-27 Gx
// 28-34 Gy
// 35-41 Gz
// 42-48 AccelMag
// 49-55 GyroMag
// =====================================================

float features[FEATURE_COUNT];

// =====================================================
// MPU6050 INITIALIZATION
// =====================================================

void writeRegister(uint8_t reg, uint8_t value) {

  Wire.beginTransmission(MPU6050_ADDR);

  Wire.write(reg);
  Wire.write(value);

  Wire.endTransmission();
}

// =====================================================
// READ 14 BYTES
//
// Accelerometer:
// AX AY AZ
//
// Temperature:
// ignored
//
// Gyroscope:
// GX GY GZ
// =====================================================

void readMPU6050(
    int16_t &rawAx,
    int16_t &rawAy,
    int16_t &rawAz,
    int16_t &rawGx,
    int16_t &rawGy,
    int16_t &rawGz
) {

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(ACCEL_XOUT_H);

  Wire.endTransmission(false);

  Wire.requestFrom(
      MPU6050_ADDR,
      14,
      true
  );

  uint8_t buffer[14];

  for (int i = 0; i < 14; i++) {

    if (Wire.available()) {
      buffer[i] = Wire.read();
    }
    else {
      buffer[i] = 0;
    }
  }

  rawAx =
      ((int16_t)buffer[0] << 8) |
      buffer[1];

  rawAy =
      ((int16_t)buffer[2] << 8) |
      buffer[3];

  rawAz =
      ((int16_t)buffer[4] << 8) |
      buffer[5];

  rawGx =
      ((int16_t)buffer[8] << 8) |
      buffer[9];

  rawGy =
      ((int16_t)buffer[10] << 8) |
      buffer[11];

  rawGz =
      ((int16_t)buffer[12] << 8) |
      buffer[13];
}

// =====================================================
// FEATURE EXTRACTION
// =====================================================

void extractAxisFeatures(
    float signal[],
    int offset
) {

  float sum = 0.0;

  float sumSquares = 0.0;

  float minimum = signal[0];

  float maximum = signal[0];

  // -----------------------------------------------
  // Mean / RMS / Min / Max
  // -----------------------------------------------

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float value = signal[i];

    sum += value;

    sumSquares += value * value;

    if (value < minimum) {
      minimum = value;
    }

    if (value > maximum) {
      maximum = value;
    }
  }

  float mean =
      sum / WINDOW_SIZE;

  float rms =
      sqrt(
          sumSquares / WINDOW_SIZE
      );

  // -----------------------------------------------
  // Variance
  // -----------------------------------------------

  float varianceSum = 0.0;

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float difference =
        signal[i] - mean;

    varianceSum +=
        difference * difference;
  }

  float variance =
      varianceSum / WINDOW_SIZE;

  float standardDeviation =
      sqrt(variance);

  float peakToPeak =
      maximum - minimum;

  // -----------------------------------------------
  // STORE
  // -----------------------------------------------

  features[offset + 0] = mean;
  features[offset + 1] = standardDeviation;
  features[offset + 2] = variance;
  features[offset + 3] = rms;
  features[offset + 4] = maximum;
  features[offset + 5] = minimum;
  features[offset + 6] = peakToPeak;
}

// =====================================================
// MAGNITUDE
// =====================================================

void calculateMagnitudes(
    float output[],
    float x[],
    float y[],
    float z[]
) {

  for (int i = 0; i < WINDOW_SIZE; i++) {

    output[i] = sqrt(
        x[i] * x[i] +
        y[i] * y[i] +
        z[i] * z[i]
    );
  }
}

// =====================================================
// FREQUENCY FEATURES
//
// The current Python MPU6050 feature pipeline does not
// include FFT-specific features, so frequency-domain
// calculations are NOT added here.
// =====================================================

// =====================================================
// COLLECT SENSOR WINDOW
// =====================================================

void collectWindow() {

  unsigned long nextSample =
      micros();

  for (int i = 0; i < WINDOW_SIZE; i++) {

    while (
        (long)(
            micros() -
            nextSample
        ) < 0
    ) {
      // Wait
    }

    int16_t rawAx;
    int16_t rawAy;
    int16_t rawAz;

    int16_t rawGx;
    int16_t rawGy;
    int16_t rawGz;

    readMPU6050(
        rawAx,
        rawAy,
        rawAz,
        rawGx,
        rawGy,
        rawGz
    );

    // =================================================
    // SENSOR SCALE
    //
    // Accelerometer:
    // ±2g -> 16384 LSB/g
    //
    // Gyroscope:
    // ±250°/s -> 131 LSB/(°/s)
    //
    // IMPORTANT:
    // These MUST match your training dataset.
    // =================================================

    ax[i] =
        ((float)rawAx) / 16384.0;

    ay[i] =
        ((float)rawAy) / 16384.0;

    az[i] =
        ((float)rawAz) / 16384.0;

    gx[i] =
        ((float)rawGx) / 131.0;

    gy[i] =
        ((float)rawGy) / 131.0;

    gz[i] =
        ((float)rawGz) / 131.0;

    nextSample +=
        SAMPLE_INTERVAL_US;
  }
}

// =====================================================
// CALCULATE ALL 56 FEATURES
// =====================================================

void calculateAllFeatures() {

  // -----------------------------------------------
  // Accelerometer
  // -----------------------------------------------

  extractAxisFeatures(
      ax,
      0
  );

  extractAxisFeatures(
      ay,
      7
  );

  extractAxisFeatures(
      az,
      14
  );

  // -----------------------------------------------
  // Gyroscope
  // -----------------------------------------------

  extractAxisFeatures(
      gx,
      21
  );

  extractAxisFeatures(
      gy,
      28
  );

  extractAxisFeatures(
      gz,
      35
  );

  // -----------------------------------------------
  // Magnitudes
  // -----------------------------------------------

  float accelerationMagnitude[
      WINDOW_SIZE
  ];

  float gyroscopeMagnitude[
      WINDOW_SIZE
  ];

  calculateMagnitudes(
      accelerationMagnitude,
      ax,
      ay,
      az
  );

  calculateMagnitudes(
      gyroscopeMagnitude,
      gx,
      gy,
      gz
  );

  extractAxisFeatures(
      accelerationMagnitude,
      42
  );

  extractAxisFeatures(
      gyroscopeMagnitude,
      49
  );
}

// =====================================================
// PRINT FEATURES
// =====================================================

void printFeatures() {

  Serial.println();
  Serial.println(
      "======================================"
  );

  Serial.println(
      "MPU6050 FEATURE VECTOR"
  );

  Serial.println(
      "======================================"
  );

  const char* names[FEATURE_COUNT] = {

    "Ax_Mean",
    "Ax_Std",
    "Ax_Variance",
    "Ax_RMS",
    "Ax_Maximum",
    "Ax_Minimum",
    "Ax_Peak_to_Peak",

    "Ay_Mean",
    "Ay_Std",
    "Ay_Variance",
    "Ay_RMS",
    "Ay_Maximum",
    "Ay_Minimum",
    "Ay_Peak_to_Peak",

    "Az_Mean",
    "Az_Std",
    "Az_Variance",
    "Az_RMS",
    "Az_Maximum",
    "Az_Minimum",
    "Az_Peak_to_Peak",

    "Gx_Mean",
    "Gx_Std",
    "Gx_Variance",
    "Gx_RMS",
    "Gx_Maximum",
    "Gx_Minimum",
    "Gx_Peak_to_Peak",

    "Gy_Mean",
    "Gy_Std",
    "Gy_Variance",
    "Gy_RMS",
    "Gy_Maximum",
    "Gy_Minimum",
    "Gy_Peak_to_Peak",

    "Gz_Mean",
    "Gz_Std",
    "Gz_Variance",
    "Gz_RMS",
    "Gz_Maximum",
    "Gz_Minimum",
    "Gz_Peak_to_Peak",

    "AccelMag_Mean",
    "AccelMag_Std",
    "AccelMag_Variance",
    "AccelMag_RMS",
    "AccelMag_Maximum",
    "AccelMag_Minimum",
    "AccelMag_Peak_to_Peak",

    "GyroMag_Mean",
    "GyroMag_Std",
    "GyroMag_Variance",
    "GyroMag_RMS",
    "GyroMag_Maximum",
    "GyroMag_Minimum",
    "GyroMag_Peak_to_Peak"
  };

  for (int i = 0; i < FEATURE_COUNT; i++) {

    Serial.print(
        names[i]
    );

    Serial.print(
        " : "
    );

    Serial.println(
        features[i],
        6
    );
  }
}

// =====================================================
// RUN MODEL
// =====================================================

void runPrediction() {

  int prediction =
      mpu6050_predict(
          features
      );

  Serial.println();

  Serial.println(
      "======================================"
  );

  Serial.println(
      "MPU6050 TINYML PREDICTION"
  );

  Serial.println(
      "======================================"
  );

  Serial.print(
      "Class ID: "
  );

  Serial.println(
      prediction
  );

  switch (prediction) {

    case 0:

      Serial.println(
          "Prediction: NORMAL"
      );

      break;

    case 1:

      Serial.println(
          "Prediction: MINOR FAULT"
      );

      break;

    case 2:

      Serial.println(
          "Prediction: MODERATE FAULT"
      );

      break;

    case 3:

      Serial.println(
          "Prediction: SEVERE FAULT"
      );

      break;

    default:

      Serial.println(
          "Prediction: UNKNOWN"
      );

      break;
  }

  Serial.println(
      "======================================"
  );
}

// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(115200);

  delay(1000);

  Wire.begin();

  // Wake MPU6050
  writeRegister(
      PWR_MGMT_1,
      0x00
  );

  delay(100);

  Serial.println();
  Serial.println(
      "PhysiCore MPU6050 TinyML"
  );

  Serial.println(
      "Arduino UNO Q"
  );

  Serial.println(
      "Initializing..."
  );

  Serial.println(
      "Ready."
  );
}

// =====================================================
// LOOP
// =====================================================

void loop() {

  Serial.println();

  Serial.println(
      "Collecting MPU6050 window..."
  );

  collectWindow();

  Serial.println(
      "Window collected."
  );

  calculateAllFeatures();

  printFeatures();

  runPrediction();

  Serial.println();

  Serial.println(
      "Next window in 2 seconds..."
  );

  delay(2000);
}
