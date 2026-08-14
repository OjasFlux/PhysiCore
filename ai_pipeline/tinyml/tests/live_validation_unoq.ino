#include "piezo_decision_tree.h"
#include <math.h>

const int PIEZO_PIN = A0;

const int WINDOW_SIZE = 100;

const unsigned long SAMPLE_INTERVAL_US = 20000;
const float SAMPLE_RATE = 50.0;

float signal[WINDOW_SIZE];
float features[9];

int windowNumber = 0;

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

  // Frequency-domain features
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

void setup() {

  Serial.begin(115200);

  delay(1000);

  pinMode(PIEZO_PIN, INPUT);

  Serial.println("PHYSICORE_UNOQ_LIVE_VALIDATION");
  Serial.println("Ready");
}

void loop() {

  unsigned long nextSampleTime = micros();

  for (int i = 0; i < WINDOW_SIZE; i++) {

    while ((long)(micros() - nextSampleTime) < 0) {
    }

    signal[i] =
        (float)analogRead(PIEZO_PIN);

    nextSampleTime +=
        SAMPLE_INTERVAL_US;
  }

  calculateFeatures();

  int prediction =
      piezo_predict(features);

  windowNumber++;

  // CSV format:
  // window,mean,std,variance,rms,max,min,p2p,frequency,energy,prediction

  Serial.print(windowNumber);
  Serial.print(",");

  Serial.print(features[0], 6);
  Serial.print(",");

  Serial.print(features[1], 6);
  Serial.print(",");

  Serial.print(features[2], 6);
  Serial.print(",");

  Serial.print(features[3], 6);
  Serial.print(",");

  Serial.print(features[4], 6);
  Serial.print(",");

  Serial.print(features[5], 6);
  Serial.print(",");

  Serial.print(features[6], 6);
  Serial.print(",");

  Serial.print(features[7], 6);
  Serial.print(",");

  Serial.print(features[8], 6);
  Serial.print(",");

  Serial.println(prediction);

  delay(100);
}
