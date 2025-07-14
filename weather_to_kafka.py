from fastapi import FastAPI
from confluent_kafka import Producer
import requests
import json
import asyncio
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

producer = Producer({'bootstrap.servers': 'localhost:9092'})
# OpenWeather api
OPENWEATHER_API_KEY = "API_KEY"
CITY = "Kolkata"

async def fetch_weather_periodically():
    while True:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            weather_data = {
                "city": CITY,
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "timestamp": data["dt"]
            }

            producer.produce(
                topic="weather_topic",
                value=json.dumps(weather_data).encode('utf-8')
            )
            producer.flush()

            print(f"Sent to Kafka: {weather_data}")

        except Exception as e:
            print(f" Error fetching or sending weather data: {e}")

        await asyncio.sleep(10)  # wait for 10 seconds

@app.on_event("startup")
async def start_background_fetch():
    asyncio.create_task(fetch_weather_periodically())

@app.get("/")
def root():
    return {"message": "Weather fetcher is running in background"}
