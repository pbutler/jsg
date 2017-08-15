
from jsg import Document
from jsg.fields import StringField, DateTimeField, HostnameField, IPv4Field
from jsg.fields import IPv6Field, URIField, EmailField

from utils import check_schema, schema
import pytest


def test_simpleschema(schema):

    @schema.add()
    class A(Document):
        a = StringField(pattern=".", default="a", min_length=1, max_length=1)

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'a': {
                        'type': 'string',
                        'pattern': ".",
                        "default": "a",
                        "minLength": 1,
                        "maxLength": 1,
                    }
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_formats(schema):

    @schema.add()
    class A(Document):
        date = DateTimeField()
        email = EmailField()
        hostname = HostnameField()
        ipv4 = IPv4Field()
        ipv6 = IPv6Field()
        uri = URIField()

    check_schema(schema, "A", {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'definitions': {
            'A': {
                'type': 'object',
                'properties': {
                    'date': {'type': 'string', 'format': "date-time"},
                    'email': {'type': 'string', 'format': "email"},
                    'hostname': {'type': 'string', 'format': "hostname"},
                    'ipv4': {'type': 'string', 'format': "ipv4"},
                    'ipv6': {'type': 'string', 'format': "ipv6"},
                    'uri': {'type': 'string', 'format': "uri"},
                },
            }
        },
        '$ref': '#/definitions/A',
    })


def test_bad_params(schema):

    with pytest.raises(TypeError):
        class A(Document):
            a = StringField(pattern=1)

    with pytest.raises(TypeError):
        class B(Document):
            a = StringField(format="something wrong")

    with pytest.raises(TypeError):
        class C(Document):
            a = StringField(min_length='a')

    with pytest.raises(TypeError):
        class D(Document):
            a = StringField(max_length='a')
