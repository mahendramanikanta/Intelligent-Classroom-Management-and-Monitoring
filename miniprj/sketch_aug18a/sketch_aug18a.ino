#define FAN_PIN D1

void setup() {
  pinMode(FAN_PIN, OUTPUT);
  analogWriteRange(1023);
}

void loop() {
  analogWrite(FAN_PIN, 1023); // 100% speed
  delay(3000);
  analogWrite(FAN_PIN, 512);  // ~50% speed
  delay(3000);
  analogWrite(FAN_PIN, 0);    // OFF
  delay(3000);
}
