from jsg import Document
from jsg.fields import StringField
from utils import check_schema, schema


def test_basic_inheritance(schema):

    @schema.add()
    class A(Document):
        a = StringField()

    @schema.add()
    class B(A):
        b = StringField()

    check_schema(schema, "B", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'B': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'string'},
                    'b': {'type': 'string'}
                },
            },
        },
        '$ref': '#/definitions/B',
    })
