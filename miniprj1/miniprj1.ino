#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>

// WiFi credentials
const char* ssid = "projectb12";
const char* password = "projectb12";

// Flask server endpoint (change IP to your PC’s local IP)
const String serverName = "http://10.56.108.30:5000/upload";  

// Sensor Pins
#define DHTPIN D1        
#define DHTTYPE DHT11
#define MQ135_PIN D0     
#define SOUND_PIN D4     
#define PIR_PIN D5      
#define IR_PIN D6        
#define LDR_PIN A0       

// Output Device Pins
#define FAN_PIN D7       
#define LIGHT_PIN D8     
#define BUZZER_PIN D3    

// Thresholds
const int TEMP_THRESHOLD = 32;      
const int HUMIDITY_THRESHOLD = 80;  
const int LDR_THRESHOLD = 200;      
const int GAS_ALERT = HIGH;         

DHT dht(DHTPIN, DHTTYPE);
WiFiClient client;

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(MQ135_PIN, INPUT);
  pinMode(SOUND_PIN, INPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(IR_PIN, INPUT);

  pinMode(FAN_PIN, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(FAN_PIN, LOW);
  digitalWrite(LIGHT_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
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
      delay(2000);
      return;
    }

    int gasValue = digitalRead(MQ135_PIN);
    int soundValue = digitalRead(SOUND_PIN);
    int pirValue = digitalRead(PIR_PIN);
    int irValue = digitalRead(IR_PIN);
    int ldrValue = analogRead(LDR_PIN);

    int fanStatus = 0;
    int lightStatus = 0;
    int buzzerStatus = 0;

    if (temperature > TEMP_THRESHOLD || humidity > HUMIDITY_THRESHOLD) {
      digitalWrite(FAN_PIN, HIGH);
      fanStatus = 1;
    } else {
      digitalWrite(FAN_PIN, LOW);
    }

    if (ldrValue < LDR_THRESHOLD) {
      digitalWrite(LIGHT_PIN, HIGH);
      lightStatus = 1;
    } else {
      digitalWrite(LIGHT_PIN, LOW);
    }

    if (gasValue == GAS_ALERT) {
      digitalWrite(BUZZER_PIN, HIGH);
      buzzerStatus = 1;
    } else {
      digitalWrite(BUZZER_PIN, LOW);
    }

    // Print all values
    Serial.println("=====================================");
    Serial.print("🌡 Temperature: "); Serial.println(temperature);
    Serial.print("💧 Humidity: "); Serial.println(humidity);
    Serial.print("💡 LDR: "); Serial.println(ldrValue);
    Serial.print("🧪 Gas: "); Serial.println(gasValue);
    Serial.print("🔊 Sound: "); Serial.println(soundValue);
    Serial.print("🚶 PIR: "); Serial.println(pirValue);
    Serial.print("👁 IR: "); Serial.println(irValue);
    Serial.print("🌀 Fan: "); Serial.println(fanStatus ? "ON" : "OFF");
    Serial.print("💡 Light: "); Serial.println(lightStatus ? "ON" : "OFF");
    Serial.println("=====================================");

    String jsonPayload = "{\"temperature\":" + String(temperature) +
                         ",\"humidity\":" + String(humidity) +
                         ",\"light_level\":" + String(ldrValue) +
                         ",\"sound_level\":" + String(soundValue) +
                         ",\"air_quality\":" + String(gasValue) +
                         ",\"pir_sensor\":" + String(pirValue) +
                         ",\"ir_sensor\":" + String(irValue) +
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

  delay(5000);
}
