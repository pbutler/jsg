
from jsg import Schema, Document
from jsg.fields import NumberField
from utils import schema, check_schema


def test_schema_ref(schema):

    @schema.add("A", title="title")
    class A(Document):
        """description"""
        a = NumberField()

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                "title": "title",
                "description": "description",
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'}
                },
            },
        },
        '$ref': '#/definitions/A',
    })
