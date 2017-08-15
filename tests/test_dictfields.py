
from jsg import Document
from jsg.fields import DictField, NumberField
from utils import check_schema, schema
import pytest


def test_empty_schema(schema):

    @schema.add()
    class A(Document):
        a = DictField()

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                "type": 'object',
                'properties': {
                    'a': {'type': 'object'}
                }
            }
        },
        '$ref': '#/definitions/A',
    })


def test_simpleschema_params(schema):

    @schema.add()
    class A(Document):
        a = DictField(
            min_properties=1,
            max_properties=2,
            properties={"a": NumberField()},
            additional_properties=NumberField(),
            pattern_properties={".*": NumberField()})

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'object',
                        "properties": {"a": {"type": "number"}},
                        "additionalProperties": {"type": "number"},
                        "patternProperties": {".*": {"type": "number"}},
                        "minProperties": 1,
                        "maxProperties": 2
                    }
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_bad_params(schema):

    with pytest.raises(TypeError):
        class A(Document):
            a = DictField(properties=1)

    # with pytest.raises(TypeError):
    #     class B(Document):
    #         a = DictField(additional_properties=1)

    with pytest.raises(TypeError):
        class C(Document):
            a = DictField(pattern_properties=1)

    with pytest.raises(TypeError):
        class D(Document):
            a = DictField(min_properties="")

    with pytest.raises(TypeError):
        class E(Document):
            a = DictField(max_properties="")
