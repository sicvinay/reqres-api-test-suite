"""Validate the suite's expectations, independently of HTTP status handling."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMAS = Path(__file__).resolve().parents[1] / "schemas"


def validate_document(document, schema_name):
    path = SCHEMAS / (schema_name + ".json")
    if path.parent.resolve() != SCHEMAS.resolve():
        raise ValueError("Invalid schema name")
    with path.open(encoding="utf-8") as stream:
        schema = json.load(stream)
    Draft202012Validator(schema).validate(document)
    return document


def response_json(response, schema_name):
    try:
        document = response.json()
    except ValueError as error:
        raise ValueError("API response is not valid JSON") from error
    return validate_document(document, schema_name)
