### IN PROGRESS ###
## USE THE 'generate_synthetic_data.py' FILE AS TEMPORARY DATA SOURCE ##

import requests
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)
cursor = conn.cursor()

cities = [
    "Quezon City",
    "Manila",
    "Davao City",
    "Caloocan",
    "Taguig",
    "Zamboanga City",
    "Cebu City",
    "Cagayan de Oro",
    "Iloilo City",
    "Bacolod",
    "Baguio",
    "Angeles City",
    "General Santos",
    "Puerto Princesa"
]

def fetch_data(City):
    try:
        weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={City},PH&units=metric&APPID={API_KEY}"
            , timeout=5)

        if weather_data.status_code == 200:
            payload = weather_data.json()
            insert_data("OpenWeatherMap", payload)
        else:
            print(City, "failed:", payload.get("message"))

    except requests.exceptions.RequestException:
        print("No internet / Request failed for", City)

def insert_data(source, payload):
    cursor.execute(
        "INSERT INTO raw_weather_data (source, payload) VALUES (%s, %s)",
        (source, Json(payload))
    )
    conn.commit()

for city in cities:
    fetch_data(city)

