#!/usr/bin/env python3
import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import json
from urllib.error import URLError
from urllib.request import urlopen, Request
from datetime import datetime

from jsonschema import validate as validate_json, SchemaError, ValidationError

CURRENT_VERSION = "v1"

DEFAULT_SCHEMA_PATH = os.path.join("data", CURRENT_VERSION, "schema.json")


def main(schema_path: str, input_path: str, check_broken_urls: bool) -> int:
    if not os.path.exists(schema_path):
        return error(f"schema not found at {schema_path}")
    if not os.path.exists(input_path):
        return error(f"input file not found at {input_path}")

    try:
        schema = json.loads(open(schema_path).read())
    except json.JSONDecodeError as e:
        return error(f"decode error: {e} (file: {schema_path})")

    try:
        data = json.loads(open(input_path).read())
    except json.JSONDecodeError as e:
        return error(f"decode error: {e} (file: {input_path})")

    try:
        validate_json(data, schema)
    except SchemaError as e:
        return error(f"bad schema: {e}")
    except ValidationError as e:
        return error(f"bad input: {e}")

    seen_ids = set()
    for fact in data:
        fact_id = fact["id"]
        if fact_id in seen_ids:
            return error(f"duplicate id: {fact_id}")
        seen_ids.add(fact_id)
        iso_date = fact["meta"]["date"].get("iso")
        if iso_date and not is_iso_date_valid(iso_date):
            return error(f"invalid date for id: {fact_id} ({iso_date})")

    if check_broken_urls:
        for fact in data:
            fact_id = fact["id"]
            image_url = fact["meta"]["image_url"]
            if is_url_broken(image_url):
                return error(f"broken image_url for id: {fact_id} ({image_url})")
            more_info_url = fact["meta"].get("more_info_url")
            if more_info_url and is_url_broken(more_info_url):
                return error(f"broken more_info_url for id: {fact_id} ({more_info_url})")

    return 0


def is_url_broken(url: str) -> bool:
    try:
        resp = urlopen(Request(url=url, method="HEAD"))
    except URLError:
        return True
    else:
        return resp.status != 200


def is_iso_date_valid(date_string: str) -> bool:
    try:
        datetime.fromisoformat(date_string)
    except ValueError:
        return False
    else:
        return True


def error(msg: str) -> int:
    print(f"fatal: {msg}")
    return 1


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Validate the Bridge Facts JSON file against the schema",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_file",
                        help="path to a file to be validated")
    parser.add_argument("-s", "--schema", metavar="path", default=DEFAULT_SCHEMA_PATH,
                        help="path to schema file")
    parser.add_argument("-b", "--broken-urls", action="store_true",
                        help="check also for broken URLs")

    args = parser.parse_args()

    sys.exit(main(
        schema_path=args.schema,
        input_path=args.input_file,
        check_broken_urls=args.broken_urls,
    ))
