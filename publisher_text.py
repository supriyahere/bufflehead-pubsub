import time
from google.cloud import pubsub_v1

# Set your project and topic
PROJECT_ID = "bufflehead-migration-analysis"
TOPIC_ID = "bufflehead-topic"

# Initialize publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_messages():
    print("Starting TEXT publisher...")

    count = 1
    while True:
        message = f"Test message {count} from text publisher"
        data = message.encode("utf-8")

        publisher.publish(topic_path, data)
        print(f"Published: {message}")

        count += 1
        time.sleep(3)  # send every 3 seconds

if __name__ == "__main__":
    publish_messages()
