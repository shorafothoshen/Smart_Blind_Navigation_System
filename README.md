# \# 🦯 Smart Blind Navigation System

# 

# An IoT-based assistive wearable/walking-stick system that helps visually impaired people move safely. It detects nearby obstacles, recognizes objects with AI, detects falls, tracks live GPS location, and gives \*\*voice and buzzer alerts\*\*, while a caregiver can monitor everything remotely from the \*\*Blynk\*\* dashboard.

# 

# \---

# 

# \## 🖼️ Project Overview

# 

# !\[Smart Blind Navigation System](images/Smart Blind Navigation System Infographic.png)

# 

# \---

# 

# \## 🎥 Demo Video

# 

# Click the image below to watch the full working demo:

# 

# \[!\[Watch the demo video](images/project-photo.png)](https://drive.google.com/file/d/13ZLQHstsLv5ax7DYjMHhBMooee33j60B/view?usp=sharing)

# 

# ▶️ \*\*\[Watch the demo on Google Drive](https://drive.google.com/file/d/13ZLQHstsLv5ax7DYjMHhBMooee33j60B/view?usp=sharing)\*\*

# 

# \---

# 

# \## ✨ Features

# 

# | Feature | Description |

# |---|---|

# | 🚧 Obstacle detection | Two ultrasonic sensors (front + side) measure distance every second |

# | 🔔 Buzzer alert | Continuous buzzer when an obstacle is \*\*≤ 15 cm\*\* |

# | 🔊 Voice warning | Spoken warning for front/side obstacle between \*\*15–40 cm\*\* (DFPlayer Mini) |

# | 📷 AI object detection | ESP32 camera sends images to a Django AI server; detected objects (person, cell phone, tv) are announced by voice |

# | 🚨 Fall detection | MPU6050 tilt angle > 90° triggers a fall alert on voice + Blynk |

# | 📍 GPS tracking | Live latitude/longitude pushed to Blynk every \~32 seconds |

# | 📱 Remote monitoring | Blynk dashboard shows distances, location, detected object, tilt, fall status and WiFi status |

# 

# \---

# 

# \## 🏗️ System Architecture

# 

# ```

# &#x20;┌────────────────────────────┐        JPEG (multipart POST)        ┌──────────────────────────┐

# &#x20;│  ESP32-S3 + Camera (OV2640)│ ──────────────────────────────────► │  AI Server (Django)      │

# &#x20;│  Smart\_Blind\_Camera        │                                     │  POST/GET /api/detect/   │

# &#x20;└────────────────────────────┘                                     │  object detection model  │

# &#x20;                                                                   └───────────┬──────────────┘

# &#x20;                                                                               │ JSON {detections:\[{object}]}

# &#x20;┌────────────────────────────┐  HTTP GET /api/detect/                          │

# &#x20;│  ESP32 (Main Controller)   │ ◄───────────────────────────────────────────────┘

# &#x20;│  Smart\_Blind\_Navigation    │

# &#x20;│  ├─ HC-SR04 ×2 (front/side)│        Wi-Fi         ┌──────────────────────────┐

# &#x20;│  ├─ MPU6050 (fall)         │ ───────────────────► │  Blynk Cloud / App       │

# &#x20;│  ├─ NEO-6M GPS             │                      │  (caregiver dashboard)   │

# &#x20;│  ├─ DFPlayer Mini + Speaker│                      └──────────────────────────┘

# &#x20;│  └─ Buzzer                 │

# &#x20;└────────────────────────────┘

# ```

# 

# The project has \*\*two microcontrollers + one server\*\*:

# 

# 1\. \*\*Main controller (ESP32)\*\* – sensors, alerts, Blynk, fetches latest detection result.

# 2\. \*\*Camera module (ESP32-S3 with camera)\*\* – captures an image every 1.5 s and uploads it to the AI server.

# 3\. \*\*AI server (Django, `ai\_server/`)\*\* – receives images, runs object detection, returns JSON.

# 

# \---

# 

# \## 🧰 Hardware Requirements

# 

# \### A) Main Controller Unit

# 

# | # | Component | Qty | Purpose |

# |---|---|---|---|

# | 1 | ESP32 DevKit (30/38-pin, ESP32-WROOM-32) | 1 | Main brain, Wi-Fi |

# | 2 | HC-SR04 ultrasonic sensor | 2 | Front \& side obstacle distance |

# | 3 | MPU6050 (GY-521) gyro/accelerometer | 1 | Fall / tilt detection |

# | 4 | NEO-6M GPS module (with antenna) | 1 | Live location |

# | 5 | DFPlayer Mini MP3 module | 1 | Voice alerts |

# | 6 | microSD card (FAT32, ≤ 32 GB) | 1 | Stores voice files |

# | 7 | Speaker 3W 4Ω / 8Ω (or earphone) | 1 | Audio output |

# | 8 | Active buzzer (5 V) | 1 | Close-range alarm |

# | 9 | 1 kΩ resistor | 1 | DFPlayer RX line protection |

# | 10 | Voltage divider resistors (1 kΩ + 2 kΩ) | 2 sets | Level-shift HC-SR04 ECHO (5 V → 3.3 V) |

# | 11 | Power: 3.7 V Li-ion/Li-Po (18650) + TP4056 + 5 V boost converter, or a 5 V power bank | 1 | Portable power |

# | 12 | Breadboard / perfboard, jumper wires, switch | – | Wiring |

# 

# \### B) Camera Unit

# 

# | # | Component | Qty | Purpose |

# |---|---|---|---|

# | 1 | ESP32-S3 camera board with \*\*PSRAM\*\* (OV2640/OV5640, pin map in `Smart\_Blind\_Camera.ino`) | 1 | Image capture + upload |

# | 2 | USB-C cable / 5 V supply | 1 | Power \& flashing |

# 

# > The camera sketch uses `XCLK=15, SIOD=4, SIOC=5, Y2–Y9 = 11,9,8,10,12,18,17,16, VSYNC=6, HREF=7, PCLK=13`. If your board has a different pin map, update those `#define`s.

# 

# \### C) Server / Network

# 

# | Item | Notes |

# |---|---|

# | PC / laptop / mini server | Runs the Django AI server (a GPU is optional but makes detection faster) |

# | Wi-Fi router or phone hotspot (2.4 GHz) | ESP32 boards, the server PC, and your phone must be reachable from each other |

# 

# \---

# 

# \## 🔌 Pin Connections (Main ESP32)

# 

# | Module | Module Pin | ESP32 Pin |

# |---|---|---|

# | Ultrasonic FRONT | TRIG | GPIO 17 |

# | | ECHO (via divider) | GPIO 16 |

# | Ultrasonic SIDE | TRIG | GPIO 5 |

# | | ECHO (via divider) | GPIO 18 |

# | Buzzer | + | GPIO 25 |

# | MPU6050 | SDA | GPIO 21 |

# | | SCL | GPIO 22 |

# | GPS NEO-6M | TX → | GPIO 32 (ESP32 RX2) |

# | | RX ← | GPIO 33 (ESP32 TX2) |

# | DFPlayer Mini | TX → | GPIO 26 (ESP32 RX) |

# | | RX ← (via 1 kΩ) | GPIO 27 (ESP32 TX) |

# | All modules | VCC / GND | 5 V (HC-SR04, DFPlayer, buzzer) / 3.3 V (MPU6050, GPS) + common GND |

# 

# > ⚠️ \*\*HC-SR04 ECHO outputs 5 V.\*\* Use a voltage divider (e.g. 1 kΩ + 2 kΩ) before connecting it to an ESP32 GPIO, or use HC-SR04P / 3.3 V-compatible sensors.

# 

# \---

# 

# \## 💻 Software Requirements

# 

# \### Arduino IDE

# 

# \- \*\*Arduino IDE 2.x\*\*

# \- \*\*ESP32 board package\*\* by Espressif (Boards Manager)

# &#x20; - Main unit board: `ESP32 Dev Module`

# &#x20; - Camera unit board: `ESP32S3 Dev Module` (enable \*\*PSRAM: OPI PSRAM\*\*, as supported by your board)

# 

# \### Arduino Libraries

# 

# | Library | Used for |

# |---|---|

# | `Blynk` (BlynkSimpleEsp32) | IoT dashboard |

# | `MPU6050\_light` | Gyro / angle reading |

# | `TinyGPSPlus` | GPS NMEA parsing |

# | `DFRobotDFPlayerMini` | Voice playback |

# | `ArduinoJson` (v6.x) | Parse API response |

# | `WiFi`, `HTTPClient`, `Wire`, `HardwareSerial` | Built into ESP32 core |

# | `esp\_camera` | Built into ESP32 core (camera unit) |

# 

# \### AI Server (`ai\_server/`)

# 

# \- Python 3.9+

# \- Django (REST endpoint `/api/detect/`)

# \- An object detection model (COCO-style labels such as `person`, `cell phone`, `tv`)

# \- `pip` packages from the server's requirements (see `ai\_server/`)

# 

# \### Mobile App

# 

# \- \*\*Blynk IoT\*\* app (Android / iOS) or Blynk web dashboard

# 

# \---

# 

# \## 🔊 DFPlayer Voice Files

# 

# Format the microSD card as \*\*FAT32\*\* and put MP3 files in the root, named exactly:

# 

# | File | Played when |

# |---|---|

# | `0001.mp3` | Wi-Fi connected / system ready |

# | `0002.mp3` | Obstacle in \*\*front\*\* (15–40 cm) |

# | `0003.mp3` | Obstacle on the \*\*side\*\* (15–40 cm) |

# | `0004.mp3` | \*\*Person\*\* detected |

# | `0005.mp3` | \*\*Cell phone\*\* detected |

# | `0006.mp3` | \*\*TV\*\* detected |

# | `0007.mp3` | \*\*Fall\*\* detected |

# 

# \---

# 

# \## 📱 Blynk Setup

# 

# 1\. Create an account at \[blynk.cloud](https://blynk.cloud) and make a \*\*Template\*\* (e.g. `smart blind navigation system`, hardware: ESP32, connection: Wi-Fi).

# 2\. Add these \*\*Datastreams\*\* and widgets:

# 

# | Virtual Pin | Data | Suggested widget |

# |---|---|---|

# | `V0` | Front distance (cm) | Gauge |

# | `V1` | Side distance (cm) | Gauge |

# | `V2` | GPS latitude | Value display / Map |

# | `V3` | GPS longitude | Value display / Map |

# | `V6` | Fall alert (0/1) | LED / Notification |

# | `V7` | Detected object (string) | Label |

# | `V8` | Tilt angle X | Value display |

# | `V9` | Tilt angle Y | Value display |

# | `V10` | Wi-Fi / API status (0/1) | LED |

# 

# 3\. Create a \*\*Device\*\* from the template and copy its `BLYNK\_TEMPLATE\_ID`, `BLYNK\_TEMPLATE\_NAME`, and `BLYNK\_AUTH\_TOKEN`.

# 

# \---

# 

# \## 🚀 Setup \& Installation

# 

# \### 1. Clone the repository

# 

# ```bash

# git clone https://github.com/shorafothoshen/Smart\_Blind\_Navigation\_System.git

# cd Smart\_Blind\_Navigation\_System

# ```

# 

# \### 2. Start the AI server

# 

# ```bash

# cd ai\_server

# python -m venv venv

# source venv/bin/activate        # Windows: venv\\Scripts\\activate

# pip install -r requirements.txt  # if provided

# python manage.py migrate

# python manage.py runserver 0.0.0.0:8000

# ```

# 

# Find your PC's local IP (`ipconfig` / `ifconfig`) – e.g. `192.168.0.10`. The API will be at `http://192.168.0.10:8000/api/detect/`.

# 

# \### 3. Configure \& upload the Main Controller sketch

# 

# Rename `Smart\_Blind\_Navigation\_System.ino.txt` → `Smart\_Blind\_Navigation\_System.ino`, open it in Arduino IDE and edit:

# 

# ```cpp

# \#define BLYNK\_TEMPLATE\_ID   "YOUR\_TEMPLATE\_ID"

# \#define BLYNK\_TEMPLATE\_NAME "YOUR\_TEMPLATE\_NAME"

# \#define BLYNK\_AUTH\_TOKEN    "YOUR\_BLYNK\_AUTH\_TOKEN"

# 

# char ssid\[] = "YOUR\_WIFI\_NAME";

# char pass\[] = "YOUR\_WIFI\_PASSWORD";

# 

# \#define API\_URL "http://<SERVER\_IP>:8000/api/detect/"

# ```

# 

# Select \*\*ESP32 Dev Module\*\* → choose the COM port → \*\*Upload\*\*.

# 

# \### 4. Configure \& upload the Camera sketch

# 

# Rename `Smart\_Blind\_Camera.ino.txt` → `Smart\_Blind\_Camera.ino` and edit:

# 

# ```cpp

# const char\* ssid      = "YOUR\_WIFI\_NAME";

# const char\* password  = "YOUR\_WIFI\_PASSWORD";

# const char\* serverUrl = "http://<SERVER\_IP>:8000/api/detect/";

# ```

# 

# Select your \*\*ESP32-S3\*\* board with PSRAM enabled → \*\*Upload\*\*.

# 

# \### 5. Power on \& test

# 

# 1\. Make sure the server PC, both ESP32 boards, and your phone are on the same network.

# 2\. Open the Serial Monitor (115200 baud) – you should see `DFPlayer OK`, `WiFi Connected`, `SYSTEM READY`.

# 3\. Open the Blynk dashboard and verify live values.

# 

# \---

# 

# \## ⚙️ How It Works

# 

# | Behaviour | Logic |

# |---|---|

# | Sensor loop | Every \*\*1 s\*\*: read front \& side ultrasonic distances → send to `V0`, `V1` |

# | Danger zone | Distance \*\*≤ 15 cm\*\* → buzzer ON |

# | Warning zone | \*\*15–40 cm\*\* → voice warning (front: `0002`, side: `0003`), played once per entry |

# | AI detection | Every \*\*1.2 s\*\* the main unit calls `/api/detect/`, reads `detections\[0].object`, shows it on `V7` and plays the matching voice |

# | Camera upload | Every \*\*1.5 s\*\* the camera unit captures a QVGA JPEG and POSTs it as `multipart/form-data` (field name `image`) |

# | Fall detection | `|AngleX| > 90°` or `|AngleY| > 90°` → `V6 = 1` + voice `0007` |

# | GPS | Location is read and pushed to `V2`/`V3` every \~32 s when a fix is available |

# 

# \### API Contract

# 

# \*\*Request (camera → server):\*\* `POST /api/detect/` with `multipart/form-data`, field `image` = JPEG.

# 

# \*\*Response (server → main unit):\*\*

# 

# ```json

# {

# &#x20; "detections": \[

# &#x20;   { "object": "person" }

# &#x20; ]

# }

# ```

# 

# \---

# 

# \## 📁 Project Structure

# 

# ```

# Smart\_Blind\_Navigation\_System/

# ├── ai\_server/                              # Django AI object-detection server

# ├── images/

# │   └── project-photo.png                   # Project photo used in this README

# ├── Smart\_Blind\_Camera.ino.txt              # ESP32-S3 camera firmware

# ├── Smart\_Blind\_Navigation\_System.ino.txt   # Main ESP32 firmware (sensors, alerts, Blynk)

# └── README.md

# ```

# 

# \---

# 

# \## 🛠️ Troubleshooting

# 

# | Problem | Fix |

# |---|---|

# | `DFPlayer FAIL` | Check SD card is FAT32, files named `0001.mp3`…, TX/RX not swapped, 1 kΩ on DFPlayer RX |

# | GPS shows `NO FIX` | Take the device outdoors with clear sky; first fix can take a few minutes |

# | `HTTP ERROR: -1` | Wrong `API\_URL`, server not running, firewall blocking port 8000, or devices on different networks |

# | `Camera Init Failed` | Wrong pin map, PSRAM not enabled, or a loose camera ribbon cable |

# | Distance always `999` | ECHO wiring/divider issue or no object in range (sensor timeout) |

# | Blynk offline | Wrong auth token/template ID, or Wi-Fi without internet access |

# 

# \---

# 

# \## 🔐 Security Note

# 

# \*\*Never commit real credentials.\*\* Wi-Fi passwords and Blynk auth tokens must not be pushed to a public repository. Keep them in a local `secrets.h` file listed in `.gitignore`, and \*\*regenerate your Blynk token\*\* if it was ever published.

# 

# \---

# 

# \## 🔮 Future Improvements

# 

# \- Emergency SMS / call to a caregiver when a fall is detected

# \- Distance estimation for detected objects and direction guidance (left/right)

# \- More object classes and multi-language voice prompts

# \- On-device (edge) detection to remove the server dependency

# \- Waterproof 3D-printed enclosure and a rechargeable battery with level indicator

# 

# \---

# 

# \## 👤 Author

# 

# \*\*shorafothoshen\*\* – \[GitHub](https://github.com/shorafothoshen)

# 

# \## 📄 License

# 

# This project is for educational purposes. Add a license of your choice (e.g. MIT) before sharing publicly.

