# Pathogen Synthetic Data Generator

An event-driven, schema-validated synthetic data generator designed to simulate environmental pathogen decay and human-surface contact interactions. This service streams structured telemetry and touch events directly to an Apache Kafka cluster integrated with Confluent Schema Registry.

---

## Features

* **Schema-Validated Events:** Enforces strict data contracts using JSON Schema and Confluent Schema Registry (`EnvironmentUpdate` and `TouchEvent`).
* **Modern Python Packaging:** Built using modern Python standards (`src/` layout) and managed via **`uv`**.
* **Containerized Deployment:** Multi-stage Docker build utilizing `python:3.14-slim` and `librdkafka` for reliable cross-platform execution.
* **Configurable Logging:** Dynamic log level control for monitoring publishing throughput in real time.

## Schemas

The generator emits two distinct event types serialized via Confluent Schema Registry using JSON Schema contracts stored in the schemas/ directory:

### Environment Update (pathogen-environment-events)
Tracks real-time fluctuations in ambient conditions for specific physical surfaces.

* event_type: String (ENVIRONMENT_UPDATE)
* surface_id: String (Unique identifier for the surface object, e.g., surf_stainless_01)
* material: String (Physical substrate category: stainless_steel, plastic, or wood)
* timestamp: Number (Epoch timestamp of the telemetry reading)
* temp: Number (Ambient temperature in Celsius, ranged 18.0 to 30.0)
* rh: Number (Relative humidity percentage, ranged 30.0 to 70.0)

### Touch Event (pathogen-touch-events)
Simulates discrete human-surface interactions and contact exposure vectors.

* event_type: String (TOUCH_EVENT)
* surface_id: String (Unique identifier for the surface object interacted with)
* material: String (Physical substrate category)
* timestamp: Number (Epoch timestamp of the contact event)
* agent_id: String (Identifier for the interacting human agent, e.g., agent_104)
---

## Repository Structure

```text
pathogen-data-generator/
├── Dockerfile
├── README.md
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── schemas/
│   ├── environment_update.json
│   └── touch_event.json
├── src/
│   └── pathogen_data_generator/
│       ├── __init__.py
│       ├── config.py
│       ├── producer.py
│       └── schemas.py
└── tests/
    ├── __init__.py
    └── test_generator.py
```

---

## Prerequisites

* Python 3.14+
* [`uv`](https://github.com/astral-sh/uv?utm_source=gemini) package manager
* Local Apache Kafka and Confluent Schema Registry (e.g., via Confluent Platform)

---

## Local Development Setup

1. **Clone the Repository & Sync Dependencies:**
```bash
git clone <repository-url>
cd pathogen-data-generator
uv sync
```


2. **Run Unit Tests:**
```bash
uv run pytest
```


3. **Run the Producer Locally:**
```bash
uv run python -m pathogen_data_generator.producer
```



---

## Configuration

The application is configured using environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker bootstrap address |
| `SCHEMA_REGISTRY_URL` | `http://localhost:8081` | Confluent Schema Registry endpoint |
| `LOG_LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## Running via Docker

1. **Build the Container Image:**
```bash
docker build -t pathogen-data-generator:latest .
```


2. **Run via Docker Compose:**
```bash
docker compose up --build
```