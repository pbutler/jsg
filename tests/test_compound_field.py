from jsg import Document
from jsg.fields import CompoundField, StringField, IntField, DocumentField
from utils import check_schema, schema


def test_compound_field(schema):

    @schema.add()
    class A(Document):
        a = CompoundField(one_of=[StringField(), IntField()])

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'oneOf': [
                            {
                                "type": "string"
                            },
                            {
                                "type": "integer"
                            }
                        ]
                    }
                },
            },
        },
        '$ref': '#/definitions/A',
    })


def test_compound_field_doc(schema):

    @schema.add()
    class A(Document):
        a = CompoundField(one_of=[StringField(), DocumentField("B")])

    @schema.add()
    class B(Document):
        b = IntField()

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'oneOf': [
                            {
                                "type": "string"
                            },
                            {
                                'type': 'object',
                                'properties': {'b': {"type": "integer"}}
                            }
                        ]
                    }
                },
            },
        },
        '$ref': '#/definitions/A',
    })
