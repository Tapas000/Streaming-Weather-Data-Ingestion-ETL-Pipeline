# 🌩️ Real-time Weather Data ETL Pipeline

![1752523893951](https://github.com/user-attachments/assets/1f281e86-aefe-4c44-b271-f7ff42929765)


This project demonstrates a real-time weather data ETL pipeline that:
- Ingests live weather data using the OpenWeatherMap API via a FastAPI service
- Streams data into Apache Kafka
- Processes the stream with Apache Spark Structured Streaming
- Stores the cleaned and structured output into SQLite

It is fully containerized using Docker and can be easily extended to production-scale systems.
# 🧰 Tools & Technologies Used

| Tool              | Role                                                        |
|-------------------|-------------------------------------------------------------|
| OpenWeatherMap API| Source of real-time weather data                            |
| FastAPI           | Lightweight REST API to fetch and push weather data to Kafka|
| Apache Kafka      | Real-time messaging system to stream data                   |
| Apache Spark      | Structured Streaming for real-time processing               |
| SQLite            | Lightweight DB to store processed weather data              |
| Docker            | Containerized deployment of all services                    |
| Bitnami Spark     | Prebuilt Spark image for simplified setup                   |
| Python            | Language used in API, producer, and Spark job logic         |

<img width="761" height="431" alt="image" src="https://github.com/user-attachments/assets/10f4c5e7-d03f-4ae5-8b69-11813dc517e7" />

# ⚙️ How the Pipeline Works

1. 🌐 FastAPI hits OpenWeatherMap API (e.g., for Kolkata) and returns weather data as JSON.
2. 📨 That data is published to Kafka topic `weather_topic` using a Python producer.
3. 🔁 Spark Structured Streaming listens to `weather_topic`, parses, transforms, and filters the data.
4. 🧱 Processed data is stored in a local SQLite database.
5. 📋 You can inspect the DB using `alerts_db.py` or any SQLite GUI.

Skills: Python • Kafka • Spark • SQL • FastAPI • Docker • Streaming Pipelines 

Create Topic for kafka consumer
 docker exec -it kafka bash
 kafka-topics --create --topic my-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
 kafka-console-producer --topic my-topic  --bootstrap-server localhost:9092
 kafka-console-consumer --topic weather_topic  --bootstrap-server localhost:9092
