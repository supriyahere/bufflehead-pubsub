import json
import time
from google.cloud import pubsub_v1

project_id = "bufflehead-migration-analysis"
topic_id = "bufflehead-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# sample messages
messages = [
    {
        "locality": "Town Dock Park, Port Washington",
        "eventdate": "2026-03-07",
        "month": 3,
        "winter_season": 2025,
        "day_of_year": 66,
        "year": 2026,
        "day": 7,
        "avg_wind_speed": 9.4,
        "avg_temp": 33.2,
        "avg_precipitation": 0.01
    },
    {
        "locality": "Town Dock, Port Washington",
        "eventdate": "2026-02-21",
        "month": 2,
        "winter_season": 2025,
        "day_of_year": 52,
        "year": 2026,
        "day": 21,
        "avg_wind_speed": 9.8,
        "avg_temp": 29.4,
        "avg_precipitation": 0.13
    }
]

for msg in messages:
    data = json.dumps(msg).encode("utf-8")
    publisher.publish(topic_path, data=data)

    print("\n" + "-" * 50)
    print("Published message:")
    print(msg)
    print("-" * 50)

    time.sleep(1)
