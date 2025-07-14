import sqlite3
import os

DB_PATH = "alerts.db"

def write_to_sqlite(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            weather_condition TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO weather_data (city, temperature, humidity, wind_speed, weather_condition, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data['city'],
        data['temperature'],
        data['humidity'],
        data['wind_speed'],
        data['weather_condition'],
        data['timestamp']
    ))

    conn.commit()
    conn.close()
