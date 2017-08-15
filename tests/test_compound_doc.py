

from jsg import Document, CompoundDocument
from jsg.fields import StringField
from utils import check_schema, schema


def test_compound_doc(schema):

    @schema.add()
    class A(Document):
        a = StringField()

    @schema.add()
    class B(Document):
        b = StringField()

    @schema.add()
    class C(CompoundDocument):
        one_of = ["A", "B"]

    check_schema(schema, "C", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'string',
                    }
                },
            },
            'B': {
                'type': 'object',
                'properties': {
                    'b': {
                        'type': 'string',
                    }
                },
            },
            'C': {
                'oneOf': [
                    {
                        '$ref': '#/definitions/A',
                    },
                    {
                        '$ref': '#/definitions/B',
                    },
                ]
            }
        },
        '$ref': '#/definitions/C',
    })


def test_compound_doc_two_types(schema):
    @schema.add()
    class A(Document):
        a = StringField()

    @schema.add()
    class B(Document):
        b = StringField()

    @schema.add()
    class C(CompoundDocument):
        one_of = ["A", "B"]
        any_of = ["A", "B"]

    check_schema(schema, "C", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'string',
                    }
                },
            },
            'B': {
                'type': 'object',
                'properties': {
                    'b': {
                        'type': 'string',
                    }
                },
            },
            'C': {
                'anyOf': [
                    {
                        '$ref': '#/definitions/A',
                    },
                    {
                        '$ref': '#/definitions/B',
                    },
                ],
                'oneOf': [
                    {
                        '$ref': '#/definitions/A',
                    },
                    {
                        '$ref': '#/definitions/B',
                    },
                ]
            }
        },
        '$ref': '#/definitions/C',
    })
