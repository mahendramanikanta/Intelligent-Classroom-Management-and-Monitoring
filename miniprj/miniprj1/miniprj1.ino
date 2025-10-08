#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "Basanth";
const char* password = "cn123456";

// Flask server POST endpoint
const String serverName = "http://192.168.62.30:5000/upload";  

// Sensor Pins
#define DHTPIN D1        
#define DHTTYPE DHT11
#define MQ135_PIN D2     
#define SOUND_PIN D4     
#define PIR_PIN D5       
#define IR_PIN D6        
#define LDR_PIN A0       

// Output Device Pins
#define FAN_PIN D7       // Fan relay
#define LIGHT_PIN D8     // Light relay
#define BUZZER_PIN D3    // Buzzer (optional)

// Thresholds
const int TEMP_THRESHOLD = 28;      // °C
const int HUMIDITY_THRESHOLD = 70;  // %
const int LDR_THRESHOLD = 500;      // Adjust by testing
const int GAS_ALERT = HIGH;         // Poor air quality signal

DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Sensor Modes
  pinMode(MQ135_PIN, INPUT);
  pinMode(SOUND_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(IR_PIN, INPUT);

  // Output Modes
  pinMode(FAN_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Default OFF state
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(LIGHT_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  // WiFi Connect
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("❌ Failed to read from DHT sensor!");
      return;
    }

    int gasValue = digitalRead(MQ135_PIN);
    int soundValue = digitalRead(SOUND_PIN);
    int pirValue = digitalRead(PIR_PIN);
    int irValue = digitalRead(IR_PIN);
    int ldrValue = analogRead(LDR_PIN);

    // ---------- AUTO CONTROL ----------
    int fanStatus = 0;
    int lightStatus = 0;
    int buzzerStatus = 0;

    // Fan control
    if (temperature > TEMP_THRESHOLD || humidity > HUMIDITY_THRESHOLD) {
      digitalWrite(FAN_PIN, HIGH);
      fanStatus = 1;
    } else {
      digitalWrite(FAN_PIN, LOW);
    }

    // Light control
    if (ldrValue < LDR_THRESHOLD) {
      digitalWrite(LIGHT_PIN, HIGH);
      lightStatus = 1;
    } else {
      digitalWrite(LIGHT_PIN, LOW);
    }

    // Gas alert control
    if (gasValue == GAS_ALERT) {
      digitalWrite(BUZZER_PIN, HIGH);
      buzzerStatus = 1;
    } else {
      digitalWrite(BUZZER_PIN, LOW);
    }

    // JSON Payload
    String jsonPayload = "{\"temperature\":" + String(temperature) +
                         ",\"humidity\":" + String(humidity) +
                         ",\"light_level\":" + String(ldrValue) +
                         ",\"sound_level\":" + String(soundValue) +
                         ",\"air_quality\":" + String(gasValue) +
                         ",\"motion\":" + String(pirValue) +
                         ",\"fan_status\":" + String(fanStatus) +
                         ",\"light_status\":" + String(lightStatus) +
                         ",\"buzzer_status\":" + String(buzzerStatus) + "}";

    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonPayload);

    Serial.print("📡 POST Response: ");
    Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("❌ WiFi Disconnected!");
  }

  delay(5000); // Wait 5 seconds before next reading
}
