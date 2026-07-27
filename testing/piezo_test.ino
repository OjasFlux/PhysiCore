const int piezoPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int value = analogRead(piezoPin);

  Serial.print("Piezo = ");
  Serial.println(value);

  delay(10);
}
