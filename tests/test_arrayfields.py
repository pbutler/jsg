from jsg import Document
from jsg.fields import ArrayField, NumberField
from utils import check_schema, schema
import pytest


def test_simpleschema_params(schema):

    @schema.add()
    class A(Document):
        a = ArrayField(min_items=1,
                       max_items=2,
                       unique_items=True,
                       items=[NumberField()], additional_items=NumberField())

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'array',
                        "minItems": 1,
                        "maxItems": 2,
                        "uniqueItems": True,
                        'items': [{'type': 'number'}],
                        'additionalItems': {'type': 'number'}
                    }
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_empty_params(schema):

    @schema.add()
    class A(Document):
        a = ArrayField()

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'array'}
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_bad_params(schema):

    with pytest.raises(TypeError):
        class A(Document):
            a = ArrayField(min_items="")

    with pytest.raises(TypeError):
        class B(Document):
            a = ArrayField(max_items="")

    with pytest.raises(TypeError):
        class C(Document):
            a = ArrayField(unique_items="")
