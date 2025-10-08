# 🧠 Intelligent Classroom Management and Monitoring System  
**A Smart IoT + AI powered solution for automating and monitoring classroom environments in real-time.**  

## 📘 Overview  
The **Intelligent Classroom Management and Monitoring System** is an IoT-based smart solution that automatically monitors and manages environmental conditions inside a classroom — such as temperature, humidity, air quality, light intensity, sound levels, and motion detection — while controlling devices like fans and lights automatically using machine learning and voice/sound commands.

---

## ⚙️ Features  
✅ Real-time monitoring of:  
- Temperature & Humidity (DHT11)  
- Air Quality (MQ135)  
- Light Intensity (LDR)  
- Sound Levels (Sound Sensor)  
- Human Presence (PIR & IR Sensors)  

✅ Automatic control of electrical devices:  
- 💡 Lights turn ON/OFF based on motion or light intensity.  
- 🌀 Fan speed & ON/OFF control based on temperature and air quality.  

✅ Intelligent Decision System:  
- Machine Learning-based prediction for optimal classroom environment control.  
- Sound-based (voice) command interpretation for manual overrides.  

✅ Cloud Connectivity:  
- NodeMCU (ESP8266) sends real-time data to a **Flask backend** via HTTP POST.  
- Data is visualized on an interactive **Streamlit dashboard**.  

---

## 🧩 System Architecture  
1. **NodeMCU (ESP8266)** – reads sensor data and sends to backend.  
2. **Flask Backend** – stores data in SQLite database and applies ML models.  
3. **Machine Learning** – predicts fan and light control logic.  
4. **Streamlit Dashboard** – displays live readings, charts, and control status.  

---

## 🧰 Components Used  
| Component | Description |
|------------|-------------|
| NodeMCU (ESP8266) | Main IoT controller |
| DHT11 | Temperature & humidity sensor |
| MQ135 | Air quality sensor |
| LDR | Light intensity detection |
| PIR Sensor | Human presence detection |
| IR Sensor | Entry/exit detection |
| Sound Sensor | Voice/sound input detection |
| Fan & Light | Output devices |
| Flask | Backend server |
| Streamlit | Dashboard visualization |
| SQLite | Local database |
| Python + ML Models | Intelligent decision logic |

---

## 💻 Installation and Setup  

### 🖥️ Backend (Flask)
1. Clone this repository  
   ```bash
   git clone https://github.com/mahendramanikanta/Intelligent-Classroom-Management-and-Monitoring.git
   cd Intelligent-Classroom-Management-and-Monitoring/backend
   ```
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server  
   ```bash
   python app.py
   ```
4. The Flask server will start at `http://<your_ipv4>:5000/`

---

### 🌐 Dashboard (Streamlit)
1. Go to the `dashboard/` folder  
2. Run  
   ```bash
   streamlit run dashboard.py
   ```
3. Access the dashboard at  
   👉 `http://localhost:8501`

---

### 📡 NodeMCU (ESP8266)
1. Open the Arduino IDE  
2. Select the correct board and COM port  
3. Upload the final `.ino` code  
4. Make sure your NodeMCU and PC are connected to the same WiFi network.  

---

## 📊 Output Example  
- Real-time data displayed on dashboard  
- Automatic switching of fan and light  
- Visualized trends for temperature, humidity, and air quality  

---

## 🧠 Future Enhancements  
- Add CO₂ and motion-based energy optimization  
- Integrate facial recognition for attendance  
- Add mobile app control and notifications  
---

## 🏁 License  
This project is licensed under the **MIT License** – feel free to use and modify with proper credits.
