from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from joblib import load
import os

app = Flask(__name__)

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
FAN_MODEL_PATH = os.path.join(BASE_DIR, "fan.pkl")
LIGHT_MODEL_PATH = os.path.join(BASE_DIR, "light.pkl")

fan_model = load(FAN_MODEL_PATH)
light_model = load(LIGHT_MODEL_PATH)

# === DB Setup ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            light_level REAL,
            sound_level REAL,
            air_quality REAL,
            pir_sensor INTEGER,
            ir_sensor INTEGER,
            ir_count INTEGER,
            fan_status INTEGER,
            light_status INTEGER,
            last_command TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Current states
fan_state = 0
light_state = 0

@app.route('/')
def home():
    return "✅ Smart Classroom Monitoring API is Running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    global fan_state, light_state
    try:
        data = request.get_json()

        temp = data.get('temperature')
        humidity = data.get('humidity')
        light = data.get('light_level')
        sound = data.get('sound_level')
        air_quality = data.get('air_quality')
        pir = data.get('pir_sensor')
        ir = data.get('ir_sensor')
        command = data.get('command')

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # IR counter
        c.execute("SELECT ir_count FROM sensor_data ORDER BY id DESC LIMIT 1")
        last = c.fetchone()
        count = last[0] if last else 0
        if ir == 1:
            count += 1

        # Command Override
        if command:
            cmd = command.lower()
            if "fan on" in cmd:
                fan_state = 1
            elif "fan off" in cmd:
                fan_state = 0
            elif "light on" in cmd:
                light_state = 1
            elif "light off" in cmd:
                light_state = 0
        else:
            # ML fallback
            features = [[temp, humidity, light, sound, pir]]
            fan_state = int(fan_model.predict(features)[0])
            light_state = int(light_model.predict(features)[0])

        # Save to DB
        c.execute('''
            INSERT INTO sensor_data (
                temperature, humidity, light_level, sound_level, air_quality,
                pir_sensor, ir_sensor, ir_count, fan_status, light_status, last_command, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            temp, humidity, light, sound, air_quality,
            pir, ir, count, fan_state, light_state, command, datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

        return jsonify({
            "status": "success",
            "fan_status": fan_state,
            "light_status": light_state,
            "last_command": command,
            "ir_count": count
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/latest', methods=['GET'])
def get_latest():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()

    data = [{
        "id": row[0],
        "temperature": row[1],
        "humidity": row[2],
        "light_level": row[3],
        "sound_level": row[4],
        "air_quality": row[5],
        "pir_sensor": row[6],
        "ir_sensor": row[7],
        "ir_count": row[8],
        "fan": row[9],
        "light": row[10],
        "last_command": row[11],
        "timestamp": row[12]
    } for row in rows]

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
