import json
from pathlib import Path


def load_schema_string(schema_filename: str) -> str:
  # Go up from schemas.py -> pathogen_data_generator -> src -> project root
  schema_path = (
      Path(__file__).resolve().parent.parent.parent
      / "schemas"
      / schema_filename
  )
  with open(schema_path, "r") as f:
    return json.dumps(json.load(f))