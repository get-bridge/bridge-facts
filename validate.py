#!/usr/bin/env python3
import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import json

import jsonschema

DEFAULT_SCHEMA_PATH = os.path.join("schemas", "bridge-facts.json")


def main(schema_path: str, input_path: str) -> int:
    if not os.path.exists(schema_path):
        return error(f"schema not found at {schema_path}")
    if not os.path.exists(input_path):
        return error(f"input file not found at {input_path}")

    schema = None
    try:
        schema = json.loads(open(schema_path).read())
    except json.JSONDecodeError as e:
        return error(f"decode error: {e} (file: {schema_path})")

    data = None
    try:
        data = json.loads(open(input_path).read())
    except json.JSONDecodeError as e:
        return error(f"decode error: {e} (file: {input_path})")

    try:
        jsonschema.validate(data, schema)
    except jsonschema.SchemaError as e:
        return error(f"bad schema: {e}")
    except jsonschema.ValidationError as e:
        return error(f"bad input: {e}")

    seen_ids = set()
    for fact in data:
        fact_id = fact["id"]
        if fact_id in seen_ids:
            return error(f"duplicate id: {fact_id}")
        seen_ids.add(fact_id)

    return 0


def error(msg: str) -> int:
    print(f"fatal: {msg}")
    return 1


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Validate the Bridge Facts JSON file against the schema",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_file", help="path to a file to be validated")
    parser.add_argument("-s", "--schema", metavar="path",
                        default=DEFAULT_SCHEMA_PATH, help="path to schema file")

    args = parser.parse_args()

    sys.exit(main(
        schema_path=args.schema,
        input_path=args.input_file,
    ))
