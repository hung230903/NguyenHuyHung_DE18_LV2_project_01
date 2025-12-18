# TOPIC
SERVER_TOPIC = "product_view"
LOCAL_TOPIC = "product_view_local_v4"

# SERVER
SERVER_BOOTSTRAP_SERVERS = "46.202.167.130:9094,46.202.167.130:9194,46.202.167.130:9294"

SERVER_SASL_CONFIG = {
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "kafka",
    "sasl.password": "UnigapKafka@2024",
}

SERVER_CONSUMER_CONFIG = {
    "bootstrap.servers": SERVER_BOOTSTRAP_SERVERS,
    "group.id": "kafka-to-kafka-group",
    "auto.offset.reset": "earliest",
    **SERVER_SASL_CONFIG
}
# LOCAL
LOCAL_BOOTSTRAP_SERVERS = "localhost:9094,localhost:9194,localhost:9294"

LOCAL_SASL_CONFIG = {
    "security.protocol": "SASL_PLAINTEXT",
    "sasl.mechanism": "PLAIN",
    "sasl.username": "admin",
    "sasl.password": "Unigap@2024",
}

LOCAL_PRODUCER_CONFIG = {
    "bootstrap.servers": LOCAL_BOOTSTRAP_SERVERS,
    "acks": "all",
    **LOCAL_SASL_CONFIG
}

LOCAL_CONSUMER_CONFIG = {
    "bootstrap.servers": LOCAL_BOOTSTRAP_SERVERS,
    "group.id": "local-kafka-to-mongo-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
    **LOCAL_SASL_CONFIG
}
