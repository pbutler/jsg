
from jsg import Document
from jsg.fields import NumberField, IntField
from utils import check_schema, schema
import pytest


def test_resolve(schema):
    @schema.add()
    class A(Document):
        a = IntField()

    schema.resolve(A)


def test_extra(schema):
    @schema.add()
    class A(Document):
        a = IntField()
        b = 1

    @schema.add()
    class B(A):
        c = IntField()
        d = 1

    check_schema(schema, "B", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'B': {
                'type': 'object',
                'properties': {
                    "a": {"type": "integer"},
                    "c": {"type": "integer"}
                }
            }
        },
        '$ref': '#/definitions/B',
    })
