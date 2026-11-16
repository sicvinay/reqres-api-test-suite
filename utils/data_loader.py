import json
from pathlib import Path

DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def load_test_data(filename, *, directory=DATA_DIRECTORY):
    root = Path(directory).resolve()
    path = (root / filename).resolve()
    if path.parent != root or path.suffix != ".json":
        raise ValueError("Use a JSON filename inside the data directory")
    try:
        with path.open(encoding="utf-8") as stream:
            data = json.load(stream)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path.name}") from error
    if not isinstance(data, dict):
        raise ValueError("Test data must be a JSON object")
    return data
