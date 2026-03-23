import json
from google.cloud import pubsub_v1
from google.cloud import bigquery

# === CONFIG ===
project_id = "bufflehead-migration-analysis"
subscription_id = "bufflehead-sub"

model_id = "bufflehead-migration-analysis.bufflehead_us.automl_bufflehead_count"

# Initialize clients
subscriber = pubsub_v1.SubscriberClient()
bq_client = bigquery.Client(project=project_id)

subscription_path = subscriber.subscription_path(project_id, subscription_id)


def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        print(f"\nReceived message: {data}")

        print("Running prediction...")

        # === IMPORTANT: avg_wind_speed MUST stay STRING ===
        query = f"""
        SELECT *
        FROM ML.PREDICT(
          MODEL `{model_id}`,
          (
            SELECT
              '{data["locality"]}' AS locality,
              DATE('{data["eventdate"]}') AS eventdate,
              {int(data["month"])} AS month,
              {int(data["winter_season"])} AS winter_season,
              {int(data["day_of_year"])} AS day_of_year,
              {int(data["year"])} AS year,
              {int(data["day"])} AS day,
              '{data["avg_wind_speed"]}' AS avg_wind_speed,
              {float(data["avg_temp"])} AS avg_temp,
              {float(data["avg_precipitation"])} AS avg_precipitation
          )
        )
        """

        query_job = bq_client.query(query)
        results = query_job.result()

        for row in results:
            print(f"Predicted bufflehead count: {row['predicted_individualcount']:.2f}")
            

        message.ack()

    except Exception as e:
        print(f"\nERROR: {e}\n")
        message.ack()   # prevent infinite loop


# Start subscriber
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
