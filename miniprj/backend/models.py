# models.py
import sqlite3

DB_NAME = "database.db"

def create_sensor_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        light_level REAL,
        sound_level REAL,
        air_quality REAL,
        motion_detected INTEGER,
        fan_status INTEGER,
        light_status INTEGER,
        timestamp TEXT
    )
    ''')

    conn.commit()
    conn.close()
