import json
import os
import random
import math
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

cities = {
    "Quezon City": {"lat": 14.6760, "lon": 121.0437},
    "Manila": {"lat": 14.5995, "lon": 120.9842},
    "Davao City": {"lat": 7.1907, "lon": 125.4553},
    "Caloocan": {"lat": 14.6507, "lon": 120.9676},
    "Taguig": {"lat": 14.5176, "lon": 121.0509},
    "Zamboanga City": {"lat": 6.9214, "lon": 122.0790},
    "Cebu City": {"lat": 10.3157, "lon": 123.8854},
    "Cagayan de Oro": {"lat": 8.4542, "lon": 124.6319},
    "Iloilo City": {"lat": 10.7202, "lon": 122.5621},
    "Bacolod": {"lat": 10.6765, "lon": 122.9509},
    "Baguio": {"lat": 16.4023, "lon": 120.5960},
    "Angeles City": {"lat": 15.1450, "lon": 120.5887},
    "General Santos": {"lat": 6.1164, "lon": 125.1716},
    "Puerto Princesa": {"lat": 9.7392, "lon": 118.7353}
}

weather_conditions = [
    ("Clear", "clear sky"),
    ("Clouds", "broken clouds"),
    ("Rain", "light rain")
]

start = datetime.now() - timedelta(days=30)

def generate_synthetic_data(city, coords, timestamp):
    main, description = random.choice(weather_conditions)
    temperature = 29.71 + 3 * math.sin(2 * math.pi * timestamp.hour / 24) + random.uniform(-1, 1)
    humidity = 80 - (temperature - 25) * 2 + random.uniform(-5, 5)

    payload = {
        "dt": int(timestamp.timestamp()),
        "id": 1692193, 
        "cod": 200, 
        "sys": {
            "id": 2008256, 
            "type": 2, 
            "sunset": 1780136466, 
            "country": "PH", 
            "sunrise": 1780089956
            }, 
        "base": "stations", 
        "main": {
            "temp": round(temperature, 2), 
            "humidity": round(max(40, min(100, humidity)), 1), 
            "pressure": 1010 + random.randint(-5, 5),
            "temp_max": round(temperature + random.uniform(0.5, 2.5), 2),
            "temp_min": round(temperature - random.uniform(0.5, 2.5), 2),
            "sea_level": 1007, 
            "feels_like": round((temperature + (humidity - 50) * 0.03 + random.uniform(-1, 1)), 2), 
            "grnd_level": 1005
        }, 
        "name": city, 
        "wind": {
            "deg": random.randint(0, 360),
            "speed": random.uniform(0, 12)
            }, 
        "coord": {
            "lat": coords["lat"],
            "lon": coords["lon"]
            }, 
        "clouds": {
            "all": random.randint(0, 100)
            }, 
        "weather": [
            {
                "id": 803, 
                "icon": "04n", 
                "main": main, 
                "description": description
            }
                ], 
        "timezone": 28800, 
        "visibility": random.randint(8000, 10000)
    }

    return payload

def insert_data(source, payload):
    cursor.execute(
        "INSERT INTO raw_weather_data (source, payload) VALUES (%s, %s)",
        (source, Json(payload))
    )
for city in cities.keys():
    for i in range(30 *24):
        timestamp = start + timedelta(hours=i)
        payload = generate_synthetic_data(city, cities[city], timestamp)
        insert_data("Synthetic", payload)
conn.commit()
    