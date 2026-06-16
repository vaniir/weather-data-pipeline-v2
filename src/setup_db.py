import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_weather_data (
        id SERIAL PRIMARY KEY,
        source TEXT,
        payload JSONB NOT NULL,
        ingested_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
cursor.close()
conn.close()