# -*- coding: UTF-8 -*-
# vim: ts=4 sts=4 sw=4 tw=100 sta et
"""%prog [options]
Python source code - @todo
"""

from collections import OrderedDict
import six

from .utils import check_role, NotInRole
from .fields import BaseField
from ._compat import Prepareable

__author__ = 'Patrick Butler'
__email__ = 'pbutler@killertux.org'
__version__ = '0.0.1'


class MetaDocument(six.with_metaclass(Prepareable, type)):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __init__(mcs, name, bases, nmspc):
        super(MetaDocument, mcs).__init__(name, bases, nmspc)

    def __new__(mcs, mcs_name, bases, attrs):
        attrs["_fields"] = OrderedDict()
        for base in bases:
            for name, attr in six.iteritems(base._fields):
                attrs["_fields"][name] = attr

        for name, attr in six.iteritems(attrs):
            if not isinstance(attr, BaseField):
                continue
            attrs["_fields"][name] = attr

        attrs = {name: attr for name, attr in six.iteritems(attrs)
                 if not isinstance(attr, BaseField)}

        klass = type.__new__(mcs, mcs_name, bases, attrs)
        return klass


class Document(six.with_metaclass(MetaDocument)):

    """A document representing an object type in JSON schema it may contain
    class variables of which inherit from BaseField and themselves represent
    the properties of this schema."""

    _fields = []
    _schema = None
    _title = None

    @classmethod
    def render(cls, schema, roles):
        """Render this document to JSON schema

        :param schema: schema that is being rendered from
        :returns: A tuple of JSON schema and a set representing the
        dependencies this schema has

        """
        ctx = OrderedDict()
        ctx["type"] = "object"
        if hasattr(cls, "_title") and cls._title:
            ctx["title"] = cls._title
        if cls.__doc__:
            ctx["description"] = cls.__doc__

        ctx["properties"] = {}
        deps = set()
        for name, field in six.iteritems(cls._fields):
            try:
                ctx["properties"][name], new_deps = field.render(schema, roles)
                deps.update(new_deps)
            except NotInRole:
                pass

        required = [k for k, v in six.iteritems(cls._fields)
                    if v.required and k in ctx["properties"]]

        if not ctx["properties"]:
            del ctx["properties"]

        if required:
            ctx["required"] = required
        return ctx, deps

    # @classmethod
    # def get_name(cls):
    #     if cls._schema is None:
    #         raise ValueError("document not associated with schema")
    #     return cls._schema._rev_registry[cls]


class CompoundDocument(Document):

    """A Document representing a compound document that uses oneOf/allOf/anyOf
    inheritance.  This class will contain three fields (one_of, all_of, and
    any_of) each of which may be defined with a string representing the name of
    the Documents that this Documents inherits from."""

    one_of = []
    all_of = []
    any_of = []

    @classmethod
    def render(cls, schema, roles):
        """Render this document to JSON schema

        :param schema: schema that is being rendered from
        :returns: A tuple of JSON schema and a set representing the
        dependencies this schema has

        """
        ctx = OrderedDict()
        deps = set()
        for compound_type in ("one_of", "all_of", "any_of"):
            name = compound_type.replace("_o", "O")
            sub_docs = getattr(cls, compound_type)
            if not sub_docs:
                continue

            ctx[name] = []
            for doc in sub_docs:
                ref = schema.get_ref_name(doc)
                deps.add(ref)
                ctx[name] += [{
                    "$ref": ref
                }]
        return ctx, deps
