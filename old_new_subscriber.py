import json
import requests
from google.cloud import pubsub_v1

# === CONFIG ===
project_id = "bufflehead-migration-analysis"
subscription_id = "bufflehead-sub"

url = "https://bufflehead-api-we2kjr3j4q-uc.a.run.app"

# === SUBSCRIBER SETUP ===
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


# === CALLBACK ===
def callback(message):
    try:
        print("\n--- New Message Received ---")

        data = json.loads(message.data.decode("utf-8"))

        print("JSON message received:")
        print(data)

        print("\nRunning prediction...")

        response = requests.post(url, json=data)

        print(f"Status Code: {response.status_code}")
        print("\nResponse from API:\n")
        print(response.text)

        message.ack()

    except Exception as e:
        print("ERROR:", e)
        message.nack()


# === MAIN ===
def main():
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=callback
    )

    print(f"Listening on {subscription_path}...\n")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()


if __name__ == "__main__":
    main()
