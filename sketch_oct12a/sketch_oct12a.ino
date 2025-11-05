// -----------------------------
// NodeMCU (ESP8266) Relay Control for Fan + Light
// D7 → Fan relay
// D8 → Light relay
// -----------------------------

#define FAN_PIN D7
#define LIGHT_PIN D8

void setup() {
  // Initialize serial monitor
  Serial.begin(9600);
  Serial.println("Fan & Light Control Started");

  // Set relay pins as output
  pinMode(FAN_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);

  // Initially turn OFF both relays (HIGH = off for most relay modules)
  digitalWrite(FAN_PIN, HIGH);
  digitalWrite(LIGHT_PIN, HIGH);
}

void loop() {
  Serial.println("Turning ON Fan and Light...");
  digitalWrite(FAN_PIN, LOW);   // Relay ON → Fan ON
  digitalWrite(LIGHT_PIN, LOW); // Relay ON → Light ON
  delay(5000); // Keep ON for 5 seconds

  Serial.println("Turning OFF Fan and Light...");
  digitalWrite(FAN_PIN, HIGH);  // Relay OFF → Fan OFF
  digitalWrite(LIGHT_PIN, HIGH); // Relay OFF → Light OFF
  delay(5000); // Keep OFF for 5 seconds
}
