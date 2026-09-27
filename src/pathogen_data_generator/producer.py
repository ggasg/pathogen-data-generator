import asyncio
import logging
import os
import random
import time
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import MessageField, SerializationContext
from pathogen_data_generator.config import (
    ENV_TOPIC_NAME,
    KAFKA_BOOTSTRAP_SERVERS,
    SCHEMA_REGISTRY_URL,
    TOUCH_TOPIC_NAME,
)
from pathogen_data_generator.schemas import load_schema_string

# Configure logging based on environment variable (default to INFO)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("PathogenProducer")

# Initialize Schema Registry and Serializers
sr_conf = {"url": SCHEMA_REGISTRY_URL}
sr_client = SchemaRegistryClient(sr_conf)

env_schema_str = load_schema_string("environment_update.json")
touch_schema_str = load_schema_string("touch_event.json")


def dict_to_env_update(obj, ctx):
  return obj


def dict_to_touch_event(obj, ctx):
  return obj


env_serializer = JSONSerializer(env_schema_str, sr_client, to_dict=dict_to_env_update)
touch_serializer = JSONSerializer(touch_schema_str, sr_client, to_dict=dict_to_touch_event)

producer_conf = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
producer = Producer(producer_conf)

# Available material surfaces to simulate touch event data on
SURFACES = [
    {"surface_id": "surf_stainless_01", "material": "stainless_steel"},
    {"surface_id": "surf_plastic_02", "material": "plastic"},
    {"surface_id": "surf_wood_03", "material": "wood"},
]


def delivery_report(err, msg):
  if err is not None:
    logger.error(f"Delivery failed for record {msg.key()}: {err}")
  else:
    logger.info(
        f"Produced to {msg.topic()} partition [{msg.partition()}] @ offset"
        f" {msg.offset()}"
    )


async def generate_stream():
  logger.info(f"Starting pathogen event stream to Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
  while True:
    timestamp = time.time()
    surface = random.choice(SURFACES)
    event_type = random.choice(["ENVIRONMENT_UPDATE", "TOUCH_EVENT"])

    if event_type == "ENVIRONMENT_UPDATE":
      payload = {
          "event_type": "ENVIRONMENT_UPDATE",
          "surface_id": surface["surface_id"],
          "material": surface["material"],
          "timestamp": timestamp,
          "temp": round(random.uniform(18.0, 30.0), 2),
          "rh": round(random.uniform(30.0, 70.0), 2),
      }
      ctx = SerializationContext(ENV_TOPIC_NAME, MessageField.VALUE)
      serialized_value = env_serializer(payload, ctx)
      producer.produce(
          ENV_TOPIC_NAME,
          key=surface["surface_id"].encode("utf-8"),
          value=serialized_value,
          callback=delivery_report,
      )
    else:
      payload = {
          "event_type": "TOUCH_EVENT",
          "surface_id": surface["surface_id"],
          "material": surface["material"],
          "timestamp": timestamp,
          "agent_id": f"agent_{random.randint(100, 150)}",
      }
      ctx = SerializationContext(TOUCH_TOPIC_NAME, MessageField.VALUE)
      serialized_value = touch_serializer(payload, ctx)
      producer.produce(
          TOUCH_TOPIC_NAME,
          key=surface["surface_id"].encode("utf-8"),
          value=serialized_value,
          callback=delivery_report,
      )

    producer.poll(0)
    await asyncio.sleep(1.0)


if __name__ == "__main__":
  asyncio.run(generate_stream())