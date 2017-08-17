# jsg
[![Build Status](https://travis-ci.org/pbutler/jsg.svg?branch=master)](https://travis-ci.org/pbutler/jsg)

Python based JSON Schema Generator currently for the draft-04 spec

## Motivations

This package aims to generate schemas for the [IETF's JSON Schema Spec](http://json-schema.org/specification-links.html#draft-4) and currently supports draft 4 of the spec.  It is the intention of the author to support newer versions of the spec as tools come out to support it.  This package was heavily inspired by the Python package [jsl](https://github.com/aromanovich/jsl) written by Anton Romanovich and which now appears to be no longer maintained as of November 2016.  The code is currently lightly documented and it is intended to be more heavily documented as development progresses.


## Installation

For now this package has not been submitted to PyPI.  Installation can be performed via:

```bash
pip install git+https://github.com/pbutler/jsg.git
```

## Example Usage

We will borrow the example from the `jsl` project's readme to show the difference in syntax.  A schema can be generated thusly:
```python
import jsg
schema = jsg.Schema("schema")

@schema.add()
class Entry(jsg.Document):
    name = jsg.StringField(required=True)

@schema.add()
class File(Entry):
    content = jsg.StringField(required=True)

@schema.add()
class Directory(Entry):
    content = jsg.ArrayField(jsg.CompoundField(one_of=[
            jsg.DocumentField("Directory", as_ref=True),
            jsg.DocumentField("File", as_ref=True)]), required=True)
    
schema.render("Directory")
```

And results with the following schema.

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "definitions": {
    "Directory": {
      "type": "object",
      "properties": {
        "content": {
          "items": {
            "oneOf": [
              {"$ref": "#/definitions/File"},
              {"$ref": "#/definitions/Directory"}
            ]
          },
          "type": "array"
        },
        "name": {"type": "string"}
      },
      "required": ["content", "name"]
    },
    "File": {
      "type": "object",
      "properties": {
        "content": {"type": "string"},
        "name": {"type": "string"}
      },
      "required": ["content", "name"]
    }
  },
  "$ref": "#/definitions/Directory"
}
```

Which in turn will validate the following json data -- this can be verified using the `jsonschema` package.

```json
{
  "name": "/",
  "content": [
    {
      "name": "/etc",
      "content": [
        {
          "name": "/etc/passwd",
          "content": "nothing to see here"
        }
      ]
    },
    {
      "name": "/vmlinuz",
      "content": "..."
    }
  ]
}
```

## Contributions
Please feel free to make contributions and log bugs via Github's issue tracker system.  To speed up integration of any pull requests please make sure changes pass the basic `tox` and `py.test` based tests and complies with the PEP8 spec.  Finally, please supply test cases to support your bugs and fixes.

## License
 This software is licensed under the [MIT License](./LICENSE).
