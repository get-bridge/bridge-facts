# Bridge Facts

## Overview

This is a part of our Hack Week project to provide the easter egg feature with interesting facts about random bridges around the world. For now [*the facts*](data.json) are stored in a single JSON file which has a [defined schema](schemas/bridge-facts.json) to ensure its validity and make sure the file served to the client is always in the correct format.

For an example of how a properly formatted data file looks like, please have a look at [`data/v1/data.sample.json`](data/v1/data.sample.json)!

## Contributing

You're welcome to help growing our database! To do so please edit [`data/v1/data.json`](data/v1/data.json) by adding new elements and opening a PR. An example of a single `Fact` element:

```json
{
  "id": "4a3ceb99-cea9-4b37-a163-0e9b6555e3d4",
  "specific_month_day": [8, 3],
  "meta": {
      "title": "Ponte Santa Trinita",
      "message": "The Ponte Santa Trìnita is the oldest elliptic arch bridge in the world, characterised by three flattened ellipses. The outside spans each measure 29 m (95 ft) with the centre span being 32 m (105 ft) in length. On the night between 3 and 4 of August 1944, the bridge was destroyed by retreating German troops on the advance of the British 8th Army. The bridge was reconstructed in 1958 with original stones raised from the Arno or taken from the same quarry of Boboli gardens, under the direction of architect Riccardo Gizdulich, who examined florentine archives, and engineer Emilio Brizzi.",
      "date": {
        "formatted": "16th century"
      },
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/The_British_Army_in_Italy_1944_NA17848.jpg/606px-The_British_Army_in_Italy_1944_NA17848.jpg",
      "more_info_url": "https://en.wikipedia.org/wiki/Ponte_Santa_Trinita"
    }
}
```

### Description

#### `id`

Must be a UUID and it's actual uniqueness within the dataset is validated. You can use:

- CLI: `uuidgen`
- VSCode plucing: [UUID Generator](https://marketplace.visualstudio.com/items?itemName=netcorext.uuid-generator)

#### `specific_month_day` (*optional*)

This is a two element array of a month and a day to help the client decide when to display the fact. This is optional since not all facts can be tied to an exact day.

#### `meta.title`, `meta.message`, `meta.date.formatted`, `meta.image_url`

These are required and displayed on the UI.

#### `meta.date.iso`

This one is optional, and requires the date to be in [ISO8601](https://www.iso.org/iso-8601-date-and-time-format.html) format, eg.:

```json
{
  "meta": {
    "date": {
      "iso": "20010406T000000+0100"
    }
  }
}
```

#### `meta.more_info_url` (*optional*)

If present, this will be shown on the UI and used to open an external browser to provide more information about the fact.

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
