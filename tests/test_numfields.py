from jsg import Document
from jsg.fields import NumberField, IntField
from utils import check_schema, schema
import pytest


def test_simpleschema_params(schema):
    @schema.add()
    class A(Document):
        a = NumberField(multiple_of=1, minimum=0, maximum=10,
                        exclusive_minimum=True, exclusive_maximum=True,
                        enum=[1, 2, 3])

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'number',
                        'multipleOf': 1,
                        'minimum': 0,
                        'maximum': 10,
                        'exclusiveMinimum': True,
                        'exclusiveMaximum': True,
                        'enum': [1, 2, 3]
                    }
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_integer_field(schema):
    @schema.add()
    class A(Document):
        a = IntField(default=0)

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'integer',
                        'default': 0
                    }
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_required(schema):
    @schema.add("A")
    class A(Document):
        a = NumberField(required=True)

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number'}
                },
                'required': ['a']
            }
        },
        '$ref': '#/definitions/A',
    })


def test_title_description(schema):
    @schema.add("A")
    class A(Document):
        a = NumberField(required=True, title="title", description="description")

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'title': 'title',
                        "description": "description",
                        'type': 'number'}
                },
                'required': ['a']
            }
        },
        '$ref': '#/definitions/A',
    })


def test_bad_params(schema):

    with pytest.raises(TypeError):
        class A(Document):
            a = NumberField(multiple_of="a")

    with pytest.raises(TypeError):
        class B(Document):
            a = NumberField(minimum="a")

    with pytest.raises(TypeError):
        class C(Document):
            a = NumberField(maximum="a")

    with pytest.raises(TypeError):
        class D(Document):
            a = NumberField(exclusive_maximum="")

    with pytest.raises(TypeError):
        class E(Document):
            a = NumberField(exclusive_minimum="")
