import json
from pathogen_data_generator.schemas import load_schema_string


def test_schema_loading():
  env_schema = load_schema_string("environment_update.json")
  parsed = json.loads(env_schema)
  assert parsed["title"] == "EnvironmentUpdate"
  assert "temp" in parsed["properties"]


def test_touch_schema_loading():
  touch_schema = load_schema_string("touch_event.json")
  parsed = json.loads(touch_schema)
  assert parsed["title"] == "TouchEvent"
  assert "agent_id" in parsed["properties"]


def test_payload_structure_keys():
  payload = {
      "event_type": "ENVIRONMENT_UPDATE",
      "surface_id": "surf_test_01",
      "material": "stainless_steel",
      "timestamp": 1727370000.0,
      "temp": 22.5,
      "rh": 45.0,
  }
  assert payload["event_type"] == "ENVIRONMENT_UPDATE"
  assert isinstance(payload["temp"], float)