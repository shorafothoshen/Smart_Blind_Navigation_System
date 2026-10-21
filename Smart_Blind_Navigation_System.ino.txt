#define BLYNK_TEMPLATE_ID "TMPL6BvRPiwR8"
#define BLYNK_TEMPLATE_NAME "smart blind navigation system"
#define BLYNK_AUTH_TOKEN "4YzZeN7qohm6MwY0RxmjxIF9LdgUImoT"

#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <MPU6050_light.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include "DFRobotDFPlayerMini.h"
#include <BlynkSimpleEsp32.h>
#include <ArduinoJson.h>

// ---------------- WIFI ----------------
char ssid[] = "LAVA LZX409I";
char pass[] = "12345678";

// ---------------- API ----------------
#define API_URL "http://10.231.206.80:8000/api/detect/"

// ---------------- MODULES ----------------
MPU6050 mpu(Wire);
TinyGPSPlus gps;

HardwareSerial gpsSerial(2);
HardwareSerial dfSerial(1);
DFRobotDFPlayerMini dfPlayer;

bool dfReady = false;

// ---------------- PINS ----------------
#define TRIG_FRONT 17
#define ECHO_FRONT 16

#define TRIG_SIDE 5
#define ECHO_SIDE 18

#define BUZZER 25

#define GPS_RX 32
#define GPS_TX 33

#define DF_RX 26
#define DF_TX 27

// ---------------- DATA ----------------
float gpsLat = 0;
float gpsLng = 0;
bool gpsFix = false;

String detectedObject = "";

unsigned long lastVoice = 0;
unsigned long lastGPSUpdate = 0;
unsigned long lastGyroPrint = 0;

bool frontPlayed = false;
bool sidePlayed = false;
bool fallDetected = false;

// ---------------- ULTRASONIC ----------------
long getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  if (duration == 0) return 999;

  return duration * 0.034 / 2;
}

// ---------------- GPS ----------------
void readGPS() {
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  if (gps.location.isValid()) {
    gpsLat = gps.location.lat();
    gpsLng = gps.location.lng();
    gpsFix = true;
  } else {
    gpsFix = false;
  }
}

void updateGPSData() {
  if (millis() - lastGPSUpdate >= 32000) {

    readGPS();

    if (gpsFix) {
      Serial.println("📍 GPS UPDATED");
      Serial.print("Lat: "); Serial.println(gpsLat, 6);
      Serial.print("Lng: "); Serial.println(gpsLng, 6);

      Blynk.virtualWrite(V2, gpsLat);
      Blynk.virtualWrite(V3, gpsLng);
    } else {
      Serial.println("GPS: NO FIX");
    }

    lastGPSUpdate = millis();
  }
}

// ---------------- DF PLAYER ----------------
void playSound(int file) {
  if (!dfReady) return;
  if (millis() - lastVoice < 1500) return;

  dfPlayer.play(file);
  lastVoice = millis();
}

// ---------------- FALL DETECTION ----------------
void checkFall() {

  mpu.update();

  float angleX = mpu.getAngleX();
  float angleY = mpu.getAngleY();

  Blynk.virtualWrite(V8, angleX);
  Blynk.virtualWrite(V9, angleY);

  if (millis() - lastGyroPrint > 500) {
    Serial.print("AngleX: "); Serial.print(angleX);
    Serial.print(" | AngleY: "); Serial.println(angleY);
    lastGyroPrint = millis();
  }

  if (abs(angleX) > 90 || abs(angleY) > 90) {

    if (!fallDetected) {
      Serial.println("🚨 FALL DETECTED!");
      Blynk.virtualWrite(V6, 1);
      playSound(7);
      fallDetected = true;
    }

  } else {
    fallDetected = false;
    Blynk.virtualWrite(V6, 0);
  }
}

// ---------------- OBJECT AUDIO ----------------
void playAudioByObject(String obj) {
  obj.toLowerCase();

  if (obj.indexOf("person") >= 0) playSound(4);
  else if (obj.indexOf("cell phone") >= 0) playSound(5);
  else if (obj.indexOf("tv") >= 0) playSound(6);
}

// ---------------- API ----------------
void fetchObjectFromAPI() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected");
    Blynk.virtualWrite(V10, 0);
    return;
  }

  Blynk.virtualWrite(V10, 1);

  WiFiClient client;
  HTTPClient http;

  http.setTimeout(800);
  http.begin(client, API_URL);

  int code = http.GET();

  if (code == 200) {

    String response = http.getString();
    response.trim();

    Serial.println("RAW RESPONSE:");
    Serial.println(response);

    DynamicJsonDocument doc(512);
    DeserializationError error = deserializeJson(doc, response);

    if (!error) {
      JsonArray detections = doc["detections"];

      if (!detections.isNull() && detections.size() > 0) {
        detectedObject = detections[0]["object"].as<String>();
      } else {
        detectedObject = "none";
      }
    } else {
      detectedObject = "unknown";
      Serial.println("JSON Parse Error");
    }

    Serial.println("========== API RESPONSE ==========");
    Serial.print("Detected Object: ");
    Serial.println(detectedObject);
    Serial.println("=================================");

    Blynk.virtualWrite(V7, detectedObject);

    playAudioByObject(detectedObject);
  }
  else {
    Serial.print("HTTP ERROR: ");
    Serial.println(code);
  }

  http.end();
}

// ---------------- SENSOR ----------------
void sendSensorData() {

  long frontDist = getDistance(TRIG_FRONT, ECHO_FRONT);
  long sideDist  = getDistance(TRIG_SIDE, ECHO_SIDE);

  if (frontDist <= 15 || sideDist <= 15) {
    digitalWrite(BUZZER, HIGH);
    frontPlayed = false;
    sidePlayed = false;
  }

  else if ((frontDist > 15 && frontDist <= 40) || (sideDist > 15 && sideDist <= 40)) {

    digitalWrite(BUZZER, LOW);

    if (frontDist > 15 && frontDist <= 40 && !frontPlayed) {
      playSound(2);
      frontPlayed = true;
    }
    if (frontDist > 40 || frontDist <= 15) frontPlayed = false;

    if (sideDist > 15 && sideDist <= 40 && !sidePlayed) {
      playSound(3);
      sidePlayed = true;
    }
    if (sideDist > 40 || sideDist <= 15) sidePlayed = false;
  }

  else {
    digitalWrite(BUZZER, LOW);
    frontPlayed = false;
    sidePlayed = false;
  }

  Blynk.virtualWrite(V0, frontDist);
  Blynk.virtualWrite(V1, sideDist);

  Serial.println("==== SENSOR DATA ====");
  Serial.print("Front: "); Serial.println(frontDist);
  Serial.print("Side: "); Serial.println(sideDist);
}

// ---------------- WIFI ----------------
void connectWiFi() {
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Blynk.virtualWrite(V10, 0);
  }

  Serial.println("\nWiFi Connected");
  Blynk.virtualWrite(V10, 1);

  if (dfReady) playSound(1);
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);

  pinMode(TRIG_FRONT, OUTPUT);
  pinMode(ECHO_FRONT, INPUT);
  pinMode(TRIG_SIDE, OUTPUT);
  pinMode(ECHO_SIDE, INPUT);
  pinMode(BUZZER, OUTPUT);

  Wire.begin(21, 22);

  mpu.begin();
  mpu.calcOffsets();

  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  dfSerial.begin(9600, SERIAL_8N1, DF_RX, DF_TX);

  delay(2000);

  if (dfPlayer.begin(dfSerial)) {
    dfPlayer.volume(30);
    dfReady = true;
    Serial.println("DFPlayer OK");
  } else {
    Serial.println("DFPlayer FAIL");
  }

  connectWiFi();
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  Serial.println("SYSTEM READY");
}

// ---------------- LOOP ----------------
void loop() {

  Blynk.run();

  static unsigned long t1 = 0;
  static unsigned long t2 = 0;

  if (millis() - t1 > 1000) {
    sendSensorData();
    t1 = millis();
  }

  if (millis() - t2 > 1200) {
    fetchObjectFromAPI();
    t2 = millis();
  }

  updateGPSData();
  checkFall();

  yield();
}