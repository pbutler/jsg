from jsg import Schema, Document
from jsg.fields import NumberField, DocumentField
from utils import schema, check_schema


def test_schema_ref(schema):

    @schema.add("A")
    class A(Document):
        a = NumberField()

    @schema.add("B")
    class B(Document):
        b = DocumentField("A", as_ref=True)

    check_schema(schema, "B", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'}
                },
            },
            'B': {
                'type': 'object',
                'properties': {
                    'b': {'$ref': '#/definitions/A'}
                },
            }
        },
        '$ref': '#/definitions/B',
    })


def test_schema_doc_inline(schema):
    @schema.add("A")
    class A(Document):
        a = NumberField()

    @schema.add("B")
    class B(Document):
        b = DocumentField("A", as_ref=False)

    check_schema(schema, "B", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'B': {
                'type': 'object',
                'properties': {
                    'b': {
                        'type': 'object',
                        'properties': {
                            'a': {'type': 'number'}
                        },
                    },
                }
            },
        },
        '$ref': '#/definitions/B',
    })
