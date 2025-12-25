import os
from dotenv import load_dotenv

load_dotenv()

# TOPICS
SERVER_TOPIC = os.getenv('SERVER_TOPIC')
LOCAL_TOPIC = os.getenv('LOCAL_TOPIC')

# BOOTSTRAP
SERVER_BOOTSTRAP_SERVERS = os.getenv('SERVER_BOOTSTRAP_SERVERS')
LOCAL_BOOTSTRAP_SERVERS = os.getenv('LOCAL_BOOTSTRAP_SERVERS')

# SASL
SERVER_SASL_CONFIG = {
    "security.protocol": os.getenv('SERVER_SECURITY_PROTOCOL'),
    "sasl.mechanism": os.getenv('SERVER_SASL_MECHANISM'),
    "sasl.username": os.getenv('SERVER_SASL_USERNAME'),
    "sasl.password": os.getenv('SERVER_SASL_PASSWORD'),
}

LOCAL_SASL_CONFIG = {
    "security.protocol": os.getenv('LOCAL_SECURITY_PROTOCOL'),
    "sasl.mechanism": os.getenv('LOCAL_SASL_MECHANISM'),
    "sasl.username": os.getenv('LOCAL_SASL_USERNAME'),
    "sasl.password": os.getenv('LOCAL_SASL_PASSWORD'),
}

# Server
SERVER_CONSUMER_CONFIG = {
    'bootstrap.servers': SERVER_BOOTSTRAP_SERVERS,
    'group.id': os.getenv('SERVER_GROUP_ID'),
    'auto.offset.reset': os.getenv('SERVER_AUTO_OFFSET_RESET'),
    **SERVER_SASL_CONFIG
}

# Local
LOCAL_PRODUCER_CONFIG = {
    'bootstrap.servers': LOCAL_BOOTSTRAP_SERVERS,
    'acks': os.getenv('LOCAL_PRODUCER_ACKS', 'all'),
    **LOCAL_SASL_CONFIG
}

LOCAL_CONSUMER_CONFIG = {
    'bootstrap.servers': LOCAL_BOOTSTRAP_SERVERS,
    'group.id': os.getenv('LOCAL_GROUP_ID'),
    'auto.offset.reset': os.getenv('LOCAL_AUTO_OFFSET_RESET'),
    'enable.auto.commit': os.getenv('LOCAL_ENABLE_AUTO_COMMIT', 'false').lower() == 'true',
    **LOCAL_SASL_CONFIG
}

# Mongo
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')