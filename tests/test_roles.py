from jsg import Document
from jsg.fields import NumberField, IntField
from utils import check_schema, schema
import pytest


def test_roles(schema):
    @schema.add()
    class A(Document):
        a = IntField(roles="test")

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'}
                },
            }
        },
        '$ref': '#/definitions/A',
    }, roles="test")


def test_roles_list(schema):
    @schema.add()
    class A(Document):
        a = IntField(roles=["test"])

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {'type': 'object'}
        },
        '$ref': '#/definitions/A',
    }, ["nottest"])


def test_roles_none_available(schema):
    @schema.add()
    class A(Document):
        a = IntField(roles="test")

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {'type': 'object'}
        },
        '$ref': '#/definitions/A',
    }, "nottest")


def test_roles_default_none_available(schema):
    @schema.add()
    class A(Document):
        a = IntField(roles="test")

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {'type': 'object'}
        },
        '$ref': '#/definitions/A',
    })
