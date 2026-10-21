#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// ================= WIFI =================
const char* ssid = "LAVA LZX409I";
const char* password = "12345678";

// ================= DJANGO API =================
const char* serverUrl = "http://10.231.206.80:8000/api/detect/";

// ================= CAMERA PINS =================
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     15
#define SIOD_GPIO_NUM     4
#define SIOC_GPIO_NUM     5

#define Y9_GPIO_NUM       16
#define Y8_GPIO_NUM       17
#define Y7_GPIO_NUM       18
#define Y6_GPIO_NUM       12
#define Y5_GPIO_NUM       10
#define Y4_GPIO_NUM       8
#define Y3_GPIO_NUM       9
#define Y2_GPIO_NUM       11

#define VSYNC_GPIO_NUM    6
#define HREF_GPIO_NUM     7
#define PCLK_GPIO_NUM     13

unsigned long lastCaptureTime = 0;
const unsigned long interval = 1500;

// ================= CAMERA INIT =================
void initCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;

  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;

  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;

  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;

  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;

  // 🔥 stable + low heat
  config.xclk_freq_hz = 8000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 18;
  config.fb_count = 1;
  config.fb_location = CAMERA_FB_IN_PSRAM;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera Init Failed");
    return;
  }

  Serial.println("Camera OK");
}

// ================= SEND IMAGE =================
void sendImageToServer() {
  camera_fb_t *fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  HTTPClient http;
  http.begin(serverUrl);

  String boundary = "----ESP32Boundary";

  String bodyStart =
      "--" + boundary + "\r\n"
      "Content-Disposition: form-data; name=\"image\"; filename=\"capture.jpg\"\r\n"
      "Content-Type: image/jpeg\r\n\r\n";

  String bodyEnd =
      "\r\n--" + boundary + "--\r\n";

  int totalLen = bodyStart.length() + fb->len + bodyEnd.length();

  // ================= SAFE FULL BUFFER =================
  uint8_t *payload = (uint8_t *)malloc(totalLen);

  if (!payload) {
    Serial.println("Memory allocation failed");
    esp_camera_fb_return(fb);
    return;
  }

  int pos = 0;

  memcpy(payload + pos, bodyStart.c_str(), bodyStart.length());
  pos += bodyStart.length();

  memcpy(payload + pos, fb->buf, fb->len);
  pos += fb->len;

  memcpy(payload + pos, bodyEnd.c_str(), bodyEnd.length());

  http.addHeader("Content-Type", "multipart/form-data; boundary=" + boundary);
  http.addHeader("Connection", "close");

  int httpCode = http.sendRequest("POST", payload, totalLen);

  free(payload);
  esp_camera_fb_return(fb);

  if (httpCode > 0) {
    String response = http.getString();

    Serial.println("===== RESPONSE =====");
    Serial.println(response);
  } 
  else {
    Serial.print("POST Failed: ");
    Serial.println(httpCode);
  }

  http.end();
}

// ================= SETUP =================
void setup() {
  Serial.begin(115200);
  delay(2000);

  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  WiFi.setTxPower(WIFI_POWER_8_5dBm);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.println(WiFi.localIP());

  initCamera();
}

// ================= LOOP =================
void loop() {
  if (millis() - lastCaptureTime >= interval) {
    lastCaptureTime = millis();
    sendImageToServer();
  }

  delay(50);
}