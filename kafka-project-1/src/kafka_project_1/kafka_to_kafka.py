import json
from confluent_kafka import Consumer, Producer
from config.settings import (
    SERVER_CONSUMER_CONFIG,
    LOCAL_PRODUCER_CONFIG,
    SERVER_TOPIC,
    LOCAL_TOPIC
)

def main():
    consumer = Consumer(SERVER_CONSUMER_CONFIG)
    producer = Producer(LOCAL_PRODUCER_CONFIG)

    consumer.subscribe([SERVER_TOPIC])

    print("Kafka → Kafka local pipeline started (manual commit)...")

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
            except json.JSONDecodeError:
                print("Invalid JSON → skipped")
                continue

            producer.produce(
                LOCAL_TOPIC,
                value=json.dumps(data),
                on_delivery=lambda err, produced_msg, consumed_msg=msg:
                    delivery_report(err, produced_msg, consumer, consumed_msg)
            )

            producer.poll(0)

    except KeyboardInterrupt:
        print("Stopping Kafka → Kafka pipeline...")

    finally:
        print("Flushing producer...")
        producer.flush()
        consumer.close()
        print("Shutdown complete.")

def delivery_report(err, produced_msg, consumer, consumed_msg):
    if err:
        print("❌ Delivery failed:", err)
        return

    try:
        consumer.commit(message=consumed_msg, asynchronous=False)

        print(
            f"Delivered to {produced_msg.topic()} "
            f"[partition {produced_msg.partition()}] "
            f"→ committed offset"
        )

    except Exception as e:
        print("Commit failed:", e)

if __name__ == "__main__":
    main()
