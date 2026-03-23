from google.cloud import pubsub_v1
import json

PROJECT_ID = "bufflehead-migration-analysis"
TOPIC_ID = "bufflehead-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

data = {
    "locality": input("Locality: "),
    "eventdate": input("Date (YYYY-MM-DD): "),
    "month": int(input("Month: ")),
    "winter_season": int(input("Winter season year: ")),
    "day_of_year": int(input("Day of year: ")),
    "year": int(input("Year: ")),
    "day": int(input("Day: ")),
    "avg_wind_speed": float(input("Wind speed: ").replace(",", ".")),
    "avg_temp": float(input("Temperature: ").replace(",", ".")),
    "avg_precipitation": float(input("Precipitation: ").replace(",", "."))
}

message = json.dumps(data).encode("utf-8")

publisher.publish(topic_path, message)

print("✅ Message published")
print("Sent:", data)
