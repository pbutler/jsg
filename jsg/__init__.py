#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: ts=4 sts=4 sw=4 tw=100 sta et
"""%prog [options]
Python source code - @todo
"""

from collections import OrderedDict
import six
from .documents import Document, CompoundDocument  # NOQA
from .fields import BaseField, IntField, NumberField, StringField  # NOQA
from .fields import DictField, ArrayField, URIField, DocumentField  # NOQA
from .fields import EmailField, HostnameField, IPv4Field, IPv6Field, DateTimeField  # NOQA

__author__ = 'Patrick Butler'
__email__ = 'pbutler@killertux.org'
__version__ = '0.0.1'


class Schema(object):

    """This defines a JSON Schema"""

    def __init__(self, name):
        """Creates a Schema Registry.  Rather than rely entirely on
        meta-classing we use decorators to specify which registry to register
        to

        :param name: string, name of registry

        """
        self._name = name
        self._registry = {}
        self._rev_registry = {}

    def add(self, definition_id=None, title=None):
        """A decorator to add a class (of subtype Document) to the schema

        :param definition_id: Name of the schema definition.
        :returns: cls, now registered

        """
        def decorator(cls):
            if definition_id is None:
                name = cls.__name__
            else:
                name = definition_id
            if title is not None:
                cls._title = title
            self._registry[name] = cls
            self._rev_registry[cls] = name
            # cls._schema = self
            # for k, v in six.iteritems(cls.__dict__):
            #     if isinstance(v, Document):
            #         print(k)
            return cls
        return decorator

    def render(self, root, roles=None):
        """Render the schema given a root element.

        :param root: Name of the root element of this schema
        :returns: A rendered schema in a python dictionary format.

        """
        if isinstance(roles, (list, tuple, set)):
            roles = set(roles)
        else:
            roles = set([roles])
        ctx = OrderedDict()
        ctx["$schema"] = "http://json-schema.org/draft-04/schema#"
        ctx["definitions"] = OrderedDict()
        ctx["$ref"] = self.get_ref_name(root)  # "#/definitions/" + root
        to_render = set([ctx["$ref"]])
        while to_render:
            ref = to_render.pop()
            name = ref.split("/")[-1]

            definition, new_deps = self._registry[name].render(self, roles)
            ctx["definitions"][name] = definition

            rendered = set(("#/definitions/" + k) for k in six.iterkeys(ctx["definitions"]))
            to_render = to_render.union(new_deps) - rendered

        return ctx

    def get_ref_name(self, cls_or_string):
        """Get the reference string given either the class name (string) or the
        class itself.

        :param cls_or_string: This param may either be a string representing
        the class name or the class itself.
        :returns: A reference string in the form of "#/defitions/<name>"

        """
        cls = self.resolve(cls_or_string)
        name = self._rev_registry[cls]
        return "#/definitions/" + name

    def resolve(self, cls_or_string):
        """Normalize the class or string represnting the class to the class
        itself

        :param cls_or_string: This param may either be a string representing
        the class name or the class itself.
        :returns: A class

        """
        if isinstance(cls_or_string, six.string_types):
            return self._registry[cls_or_string]
        else:
            return cls_or_string
