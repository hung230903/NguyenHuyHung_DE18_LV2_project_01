import json
from confluent_kafka import Consumer
from pymongo import MongoClient, errors

from config.settings import (
    LOCAL_CONSUMER_CONFIG,
    LOCAL_TOPIC,
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME
)

BATCH_SIZE = 300

def main():
    consumer = Consumer(LOCAL_CONSUMER_CONFIG)
    consumer.subscribe([LOCAL_TOPIC])

    mongo_client = MongoClient(MONGO_URI)
    collection = mongo_client[DB_NAME][COLLECTION_NAME]

    batch = []
    last_msg = None

    print("Kafka local → MongoDB started...")

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error:", msg.error())
                continue

            try:
                data = json.loads(msg.value().decode("utf-8"))
                data["_id"] = data["id"]
                batch.append(data)
                last_msg = msg

            except json.JSONDecodeError:
                print("Invalid JSON → skipped")
                continue

            if len(batch) >= BATCH_SIZE:
                flush_batch(collection, batch)
                consumer.commit(message=last_msg, asynchronous=False)
                batch.clear()

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        if batch:
            flush_batch(collection, batch)
            consumer.commit(message=last_msg, asynchronous=False)

        consumer.close()
        mongo_client.close()
        print("Shutdown complete.")

def flush_batch(collection, batch):
    try:
        collection.insert_many(batch, ordered=False)
        print(f"Inserted batch: {len(batch)}")

    except errors.BulkWriteError as e:
        write_errors = e.details.get("writeErrors", [])
        dup_count = sum(1 for err in write_errors if err.get("code") == 11000)

        print(
            f"Batch processed: "
            f"{len(batch) - dup_count} inserted, "
            f"{dup_count} duplicates (idempotent)"
        )

    except Exception as e:
        print("Mongo error, batch NOT committed:", e)
        raise


if __name__ == "__main__":
    main()
