#include "piezo_decision_tree.h"
#include <math.h>

// =====================================================
// PhysiCore - Embedded Piezo TinyML
// Target: Arduino Nano / ATmega328P
//
// Window:
//   100 samples
//
// Sampling:
//   50 Hz
//
// Features:
//   0  Mean
//   1  Std
//   2  Variance
//   3  RMS
//   4  Maximum
//   5  Minimum
//   6  Peak_to_Peak
//   7  Dominant_Frequency
//   8  Spectral_Energy
// =====================================================

// -----------------------------------------------------
// SENSOR
// -----------------------------------------------------

const int PIEZO_PIN = A0;

// -----------------------------------------------------
// SAMPLING
// -----------------------------------------------------

const int WINDOW_SIZE = 100;

const unsigned long SAMPLE_INTERVAL_US = 20000;
// 20,000 us = 20 ms = 50 Hz

const float SAMPLE_RATE = 50.0;

// -----------------------------------------------------
// SIGNAL BUFFER
// -----------------------------------------------------

float signal[WINDOW_SIZE];

// -----------------------------------------------------
// FEATURE VECTOR
// -----------------------------------------------------

float feature_vector[9];

// -----------------------------------------------------
// COLLECT WINDOW
// -----------------------------------------------------

void collect_window() {

  unsigned long next_sample_time = micros();

  for (int i = 0; i < WINDOW_SIZE; i++) {

    while ((long)(micros() - next_sample_time) < 0) {
      // Wait for the exact sample time
    }

    signal[i] = (float)analogRead(PIEZO_PIN);

    next_sample_time += SAMPLE_INTERVAL_US;
  }
}

// -----------------------------------------------------
// CALCULATE BASIC FEATURES
// -----------------------------------------------------

void calculate_time_features() {

  float sum = 0.0;

  float sum_squares = 0.0;

  float minimum = signal[0];

  float maximum = signal[0];

  // -----------------------------------------------
  // Mean, Min, Max, Sum of Squares
  // -----------------------------------------------

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float x = signal[i];

    sum += x;

    sum_squares += x * x;

    if (x < minimum) {
      minimum = x;
    }

    if (x > maximum) {
      maximum = x;
    }
  }

  float mean = sum / WINDOW_SIZE;

  // -----------------------------------------------
  // Variance and Standard Deviation
  // Match numpy.var() / numpy.std()
  // -----------------------------------------------

  float variance_sum = 0.0;

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float difference = signal[i] - mean;

    variance_sum += difference * difference;
  }

  float variance =
      variance_sum / WINDOW_SIZE;

  float standard_deviation =
      sqrt(variance);

  // -----------------------------------------------
  // RMS
  // -----------------------------------------------

  float rms =
      sqrt(sum_squares / WINDOW_SIZE);

  // -----------------------------------------------
  // Peak-to-Peak
  // -----------------------------------------------

  float peak_to_peak =
      maximum - minimum;

  // -----------------------------------------------
  // Store features
  // -----------------------------------------------

  feature_vector[0] = mean;
  feature_vector[1] = standard_deviation;
  feature_vector[2] = variance;
  feature_vector[3] = rms;
  feature_vector[4] = maximum;
  feature_vector[5] = minimum;
  feature_vector[6] = peak_to_peak;
}

// -----------------------------------------------------
// FREQUENCY FEATURES
//
// Equivalent concept to the Python:
//   signal - mean
//   rfft()
//   ignore DC component
//   dominant frequency
//   spectral energy
//
// Uses a direct DFT because the window is only 100 samples.
// This avoids needing an external FFT library.
// -----------------------------------------------------

void calculate_frequency_features() {

  float mean = feature_vector[0];

  float max_magnitude = -1.0;

  float dominant_frequency = 0.0;

  float spectral_energy = 0.0;

  // Positive-frequency bins:
  // 0 ... WINDOW_SIZE / 2

  for (int k = 0; k <= WINDOW_SIZE / 2; k++) {

    float real_part = 0.0;
    float imag_part = 0.0;

    for (int n = 0; n < WINDOW_SIZE; n++) {

      float centered =
          signal[n] - mean;

      float angle =
          2.0 * PI * k * n / WINDOW_SIZE;

      real_part +=
          centered * cos(angle);

      imag_part -=
          centered * sin(angle);
    }

    float magnitude =
        sqrt(
            (real_part * real_part) +
            (imag_part * imag_part)
        );

    // Match Python behavior:
    // DC component is ignored.
    if (k == 0) {
      magnitude = 0.0;
    }

    // Spectral energy
    spectral_energy +=
        magnitude * magnitude;

    // Dominant frequency
    if (magnitude > max_magnitude) {

      max_magnitude = magnitude;

      dominant_frequency =
          ((float)k * SAMPLE_RATE) /
          WINDOW_SIZE;
    }
  }

  feature_vector[7] =
      dominant_frequency;

  feature_vector[8] =
      spectral_energy;
}

// -----------------------------------------------------
// CALCULATE ALL FEATURES
// -----------------------------------------------------

void calculate_features() {

  calculate_time_features();

  calculate_frequency_features();
}

// -----------------------------------------------------
// DISPLAY FEATURES
// -----------------------------------------------------

void print_features() {

  Serial.println();
  Serial.println("FEATURE VECTOR");

  Serial.print("Mean              : ");
  Serial.println(feature_vector[0], 4);

  Serial.print("Std               : ");
  Serial.println(feature_vector[1], 4);

  Serial.print("Variance          : ");
  Serial.println(feature_vector[2], 4);

  Serial.print("RMS               : ");
  Serial.println(feature_vector[3], 4);

  Serial.print("Maximum           : ");
  Serial.println(feature_vector[4], 4);

  Serial.print("Minimum           : ");
  Serial.println(feature_vector[5], 4);

  Serial.print("Peak-to-Peak      : ");
  Serial.println(feature_vector[6], 4);

  Serial.print("Dominant Frequency: ");
  Serial.println(feature_vector[7], 4);

  Serial.print("Spectral Energy   : ");
  Serial.println(feature_vector[8], 4);
}

// -----------------------------------------------------
// RUN MODEL
// -----------------------------------------------------

void run_model() {

  int prediction =
      piezo_predict(feature_vector);

  Serial.println();
  Serial.println("================================");
  Serial.println("PIEZ0 TINYML PREDICTION");
  Serial.println("================================");

  Serial.print("Class ID: ");
  Serial.println(prediction);

  switch (prediction) {

    case 0:
      Serial.println("Prediction: NORMAL");
      break;

    case 1:
      Serial.println("Prediction: MINOR FAULT");
      break;

    case 2:
      Serial.println("Prediction: MODERATE FAULT");
      break;

    case 3:
      Serial.println("Prediction: SEVERE FAULT");
      break;

    default:
      Serial.println("Prediction: UNKNOWN");
      break;
  }

  Serial.println("================================");
}

// -----------------------------------------------------
// SETUP
// -----------------------------------------------------

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("PhysiCore Piezo TinyML");
  Serial.println("Initializing...");

  pinMode(PIEZO_PIN, INPUT);

  Serial.println("Ready.");
}

// -----------------------------------------------------
// LOOP
// -----------------------------------------------------

void loop() {

  Serial.println();
  Serial.println("Collecting 100 samples...");

  collect_window();

  Serial.println("Window collected.");

  calculate_features();

  print_features();

  run_model();

  Serial.println();
  Serial.println("Next window in 2 seconds...");

  delay(2000);
}
