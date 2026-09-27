import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")
ENV_TOPIC_NAME = "pathogen-environment-events"
TOUCH_TOPIC_NAME = "pathogen-touch-events"