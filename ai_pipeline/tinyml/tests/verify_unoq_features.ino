#include "piezo_decision_tree.h"
#include <math.h>

const int WINDOW_SIZE = 100;
const float SAMPLE_RATE = 50.0;

float signal[WINDOW_SIZE];
float features[9];

int sampleCount = 0;

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println("UNO Q FEATURE VERIFICATION");
  Serial.println("Ready for 100 samples");
}

void calculateFeatures() {

  float sum = 0.0;
  float sumSquares = 0.0;

  float minimum = signal[0];
  float maximum = signal[0];

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float x = signal[i];

    sum += x;
    sumSquares += x * x;

    if (x < minimum) {
      minimum = x;
    }

    if (x > maximum) {
      maximum = x;
    }
  }

  float mean = sum / WINDOW_SIZE;

  float varianceSum = 0.0;

  for (int i = 0; i < WINDOW_SIZE; i++) {

    float diff = signal[i] - mean;

    varianceSum += diff * diff;
  }

  float variance =
      varianceSum / WINDOW_SIZE;

  float standardDeviation =
      sqrt(variance);

  float rms =
      sqrt(sumSquares / WINDOW_SIZE);

  float peakToPeak =
      maximum - minimum;

  features[0] = mean;
  features[1] = standardDeviation;
  features[2] = variance;
  features[3] = rms;
  features[4] = maximum;
  features[5] = minimum;
  features[6] = peakToPeak;

  float maxMagnitude = -1.0;
  float dominantFrequency = 0.0;
  float spectralEnergy = 0.0;

  for (int k = 0; k <= WINDOW_SIZE / 2; k++) {

    float realPart = 0.0;
    float imagPart = 0.0;

    for (int n = 0; n < WINDOW_SIZE; n++) {

      float centered =
          signal[n] - mean;

      float angle =
          2.0 * PI * k * n / WINDOW_SIZE;

      realPart +=
          centered * cos(angle);

      imagPart -=
          centered * sin(angle);
    }

    float magnitude =
        sqrt(
            realPart * realPart +
            imagPart * imagPart
        );

    if (k == 0) {
      magnitude = 0.0;
    }

    spectralEnergy +=
        magnitude * magnitude;

    if (magnitude > maxMagnitude) {

      maxMagnitude = magnitude;

      dominantFrequency =
          ((float)k * SAMPLE_RATE) /
          WINDOW_SIZE;
    }
  }

  features[7] = dominantFrequency;
  features[8] = spectralEnergy;
}

void printResults() {

  Serial.println();
  Serial.println("================================");
  Serial.println("UNO Q FEATURES");
  Serial.println("================================");

  Serial.print("Mean               : ");
  Serial.println(features[0], 6);

  Serial.print("Std                : ");
  Serial.println(features[1], 6);

  Serial.print("Variance           : ");
  Serial.println(features[2], 6);

  Serial.print("RMS                : ");
  Serial.println(features[3], 6);

  Serial.print("Maximum            : ");
  Serial.println(features[4], 6);

  Serial.print("Minimum            : ");
  Serial.println(features[5], 6);

  Serial.print("Peak-to-Peak       : ");
  Serial.println(features[6], 6);

  Serial.print("Dominant Frequency : ");
  Serial.println(features[7], 6);

  Serial.print("Spectral Energy    : ");
  Serial.println(features[8], 6);

  int prediction =
      piezo_predict(features);

  Serial.println();
  Serial.print("Prediction Class: ");
  Serial.println(prediction);

  Serial.println("================================");
}

void loop() {

  if (Serial.available()) {

    String line =
        Serial.readStringUntil('\n');

    line.trim();

    if (line.length() == 0) {
      return;
    }

    float value =
        line.toFloat();

    signal[sampleCount] = value;

    sampleCount++;

    if (sampleCount >= WINDOW_SIZE) {

      Serial.println("100 samples received.");

      calculateFeatures();

      printResults();

      sampleCount = 0;

      Serial.println();
      Serial.println("READY FOR NEXT 100 SAMPLES");
    }
  }
}
