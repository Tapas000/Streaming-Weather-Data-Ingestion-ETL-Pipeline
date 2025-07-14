from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType
from sqlite_db import write_to_sqlite

# Define schema
schema = StructType() \
    .add("city", StringType()) \
    .add("temperature", DoubleType()) \
    .add("humidity", DoubleType()) \
    .add("wind_speed", DoubleType()) \
    .add("weather_condition", StringType()) \
    .add("timestamp", StringType())

# Start Spark session
spark = SparkSession.builder \
    .appName("WeatherDataProcessor") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read stream from Kafka topic
df_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather_topic") \
    .option("startingOffsets", "latest") \
    .load()

# Parse Kafka value as JSON
df_json = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Write to SQLite
def process_batch(batch_df, epoch_id):
    records = batch_df.collect()
    for row in records:
        write_to_sqlite(row.asDict())

query = df_json.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

query.awaitTermination()
