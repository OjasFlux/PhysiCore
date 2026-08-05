#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

unsigned long startTime;

void setup() {
  Serial.begin(115200);

  if (!mpu.begin()) {
    while (1);
  }

  startTime = millis();
}

void loop() {
  sensors_event_t a, g, temp;

  mpu.getEvent(&a, &g, &temp);

  Serial.print(millis() - startTime);
  Serial.print(",");

  Serial.print(a.acceleration.x);
  Serial.print(",");

  Serial.print(a.acceleration.y);
  Serial.print(",");

  Serial.print(a.acceleration.z);
  Serial.print(",");

  Serial.print(g.gyro.x);
  Serial.print(",");

  Serial.print(g.gyro.y);
  Serial.print(",");

  Serial.println(g.gyro.z);

  delay(20);
}
