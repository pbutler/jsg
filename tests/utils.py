import json
import pytest
import jsg
import jsonschema


def check_schema(schema, root, correct, roles=None):
    skema = json.loads(json.dumps((schema.render(root=root, roles=roles))))
    jsonschema.validate(skema, json.load(open("tests/hyperschema.json", "rt")))
    print(skema)
    assert skema == correct


@pytest.fixture(scope="module")
def schema():
    return jsg.Schema("schema")
