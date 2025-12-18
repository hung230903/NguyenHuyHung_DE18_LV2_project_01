import json
from confluent_kafka import Consumer, Producer
from kafka_project_1.config.kafka import (
    SERVER_CONSUMER_CONFIG,
    LOCAL_PRODUCER_CONFIG,
    SERVER_TOPIC,
    LOCAL_TOPIC
)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to {msg.topic()} "
            f"[partition {msg.partition()}]"
        )

def main():
    consumer = Consumer(SERVER_CONSUMER_CONFIG)
    producer = Producer(LOCAL_PRODUCER_CONFIG)

    consumer.subscribe([SERVER_TOPIC])
    print("Kafka → Kafka local pipeline started...")

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

            producer.produce(
                LOCAL_TOPIC,
                value=json.dumps(data),
                callback=delivery_report
            )
            producer.poll(0)

    except KeyboardInterrupt:
        print("Stopping Kafka → Kafka local pipeline...")
    finally:
        consumer.close()
        producer.flush()

if __name__ == "__main__":
    main()
