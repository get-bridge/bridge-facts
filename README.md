# Bridge Facts

## Overview

This is a part of our Hackweek project to provide the easter egg feature with interesting facts about random bridges around the world. For now [_the facts_](data.json) are stored in a single JSON file which has a [defined schema](schemas/bridge-facts.json) to ensure its validity and make sure the file served to the client is always in the correct format.

For an example of how a properly formatted data file looks like, please have a look at [`data.sample.json`](data.sample.json).

## Validating the data file

The script [`validate.py`](validate.py) can be used to validate both the data file against the schema and the provided schema itself. This can be useful for PR checks and other automation tasks. When the input file is valid, no output will be generated and the program will exit normally with status code 0.

### Dependencies

* [`jsonschema`](https://github.com/python-jsonschema/jsonschema)

### Usage

```
usage: validate.py [-h] [-s path] [-b] input_file

Validate the Bridge Facts JSON file against the schema

positional arguments:
  input_file            path to a file to be validated

optional arguments:
  -h, --help            show this help message and exit
  -s path, --schema path
                        path to schema file (default: schemas/bridge-facts.json)
  -b, --broken-urls     check also for broken URLs (default: False)
```
