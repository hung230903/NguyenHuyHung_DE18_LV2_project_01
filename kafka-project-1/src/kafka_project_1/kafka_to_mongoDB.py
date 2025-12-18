import json
from confluent_kafka import Consumer
from pymongo import MongoClient, errors
from kafka_project_1.config.kafka import LOCAL_CONSUMER_CONFIG, LOCAL_TOPIC
from kafka_project_1.config.mongoDB import MONGO_URI, DB_NAME, COLLECTION_NAME

def main():
    consumer = Consumer(LOCAL_CONSUMER_CONFIG)
    consumer.subscribe([LOCAL_TOPIC])

    mongo_client = MongoClient(MONGO_URI)
    collection = mongo_client[DB_NAME][COLLECTION_NAME]

    print("Kafka local → MongoDB pipeline started...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            try:
                data = json.loads(msg.value().decode("utf-8"))
            except json.JSONDecodeError:
                print("Invalid JSON, skipping message.")
                continue

            try:
                collection.insert_one(data)
                print("Inserted:", data)
            except errors.PyMongoError as e:
                print(f"MongoDB insert error: {e}")

    except KeyboardInterrupt:
        print("Stopping Kafka local → MongoDB pipeline...")
    finally:
        consumer.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
