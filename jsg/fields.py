# vim: ts=4 sts=4 sw=4 tw=100 sta et

from collections import OrderedDict
import six
from .utils import check_role


def is_number(num):
    return isinstance(num, (int, float))


class BaseField(object):

    """Base class for all fields that are represented in the JSON Schema"""

    def __init__(self, id='', name=None, default=None, enum=None, title=None,
                 description=None, required=False, roles=None):
        """TODO: to be defined1.

        :param id: TODO
        :param name: a name that overrides
        :param default: default value for the field
        :param enum: a list of possible values
        :param title: a title to go along with the field
        :param description: a long form description to go along with the field
        :param required: whether this field should be required

        """
        self.id = id
        self.name = name
        self.required = required
        if roles:
            if isinstance(roles, (list, tuple, set)):
                self._roles = set(roles)
            else:
                self._roles = set([roles])
        else:
            self._roles = set()

        if not hasattr(self, "_attrs"):
            self._attrs = {}

        if title is not None:
            self._attrs["title"] = title
        if description is not None:
            self._attrs["description"] = description
        if default is not None:
            self._attrs["default"] = default
        if enum is not None:
            self._attrs["enum"] = enum

    def render(self, schema, roles):
        check_role(self._roles, roles)
        ctx = OrderedDict()
        ctx.update(self._attrs)
        return ctx, set()


class NumberField(BaseField):

    """A field representing a number (float or int) field"""

    def __init__(self, multiple_of=None, minimum=None, exclusive_minimum=None, maximum=None,
                 exclusive_maximum=None, **kwargs):
        """An number field representation in the JSON Schema

        :param multiple_of: number must be multiple of this number
        :param minimum: minimum value
        :param exclusive_minimum: should minimum be inclusive or exclusive
        :param maximum: maximum value
        :param exclusive_maximum: should maximum be inclusive or exclusive

        """
        super(NumberField, self).__init__(**kwargs)
        if multiple_of is not None:
            if not is_number(multiple_of):
                raise TypeError("multiple_of must be a number")
            self._attrs["multipleOf"] = multiple_of
        if minimum is not None:
            if not is_number(minimum):
                raise TypeError("minimum must be a number")
            self._attrs["minimum"] = minimum
        if exclusive_minimum is not None:
            if not isinstance(exclusive_minimum, bool):
                raise TypeError("exclusive_minimum must be a number")
            self._attrs["exclusiveMinimum"] = exclusive_minimum
        if maximum is not None:
            if not is_number(maximum):
                raise TypeError("maximum must be a number")
            self._attrs["maximum"] = maximum
        if exclusive_maximum is not None:
            if not isinstance(exclusive_maximum, bool):
                raise TypeError("exclusive_maximum must be a number")
            self._attrs["exclusiveMaximum"] = exclusive_maximum

        # Noneset(kwargs.keys())
        self._attrs["type"] = "number"


class IntField(NumberField):

    """A field representing a number (integer only) field"""

    def __init__(self, **kwargs):
        """An integer field representation in the JSON Schema

        :param multiple_of: number must be multiple of this number
        :param minimum: minimum value
        :param exclusive_minimum: should minimum be inclusive or exclusive
        :param maximum: maximum value
        :param exclusive_maximum: should maximum be inclusive or exclusive

        """
        super(IntField, self).__init__(**kwargs)
        self._attrs["type"] = "integer"


class StringField(BaseField):

    """A field representing a string."""

    def __init__(self, pattern=None, format=None, min_length=None,
                 max_length=None, **kwargs):
        """TODO: to be defined1.

        :param pattern: TODO
        :param format: TODO
        :param min_length: TODO
        :param max_length: TODO

        """
        super(StringField, self).__init__(**kwargs)

        self._attrs["type"] = "string"

        if pattern is not None:
            if not isinstance(pattern, six.string_types):
                raise TypeError("pattern must be a string")
            self._attrs["pattern"] = pattern
        if format is not None:
            if format not in ("date-time", "email", "hostname", "ipv4", "ipv6", "uri"):
                raise TypeError("format must be a string")
            self._attrs["format"] = format
        if min_length is not None:
            if not isinstance(min_length, int):
                raise TypeError("min_length must be an int")
            self._attrs["minLength"] = min_length
        if max_length is not None:
            if not isinstance(max_length, int):
                raise TypeError("max_length must be an int")
            self._attrs["maxLength"] = max_length


class DateTimeField(StringField):
    """A string instance is valid against this attribute if it is a valid
       date representation as defined by RFC 3339, section 5.6 [RFC3339]."""

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        """
        super(DateTimeField, self).__init__(format="date-time", **kwargs)


class EmailField(StringField):

    """ A string instance is valid against this attribute if it is a valid
       Internet email address as defined by RFC 5322, section 3.4.1
       RFC5322."""

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        """
        super(EmailField, self).__init__(format="email", **kwargs)


class HostnameField(StringField):
    """A string instance is valid against this attribute if it is a valid
       representation for an Internet host name, as defined by RFC 1034,
       section 3.1 RFC1034."""

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        """
        super(HostnameField, self).__init__(format="hostname", **kwargs)


class IPv4Field(StringField):
    """A string instance is valid against this attribute if it is a valid
       representation of an IPv4 address according to the "dotted-quad" ABNF
       syntax as defined in RFC 2673, section 3.2 RFC2673."""

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        """
        super(IPv4Field, self).__init__(format="ipv4", **kwargs)


class IPv6Field(StringField):
    """A string instance is valid against this attribute if it is a valid
       representation of an IPv6 address as defined in RFC 2373, section 2.2
       RFC2373."""

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        """
        super(IPv6Field, self).__init__(format="ipv6", **kwargs)


class URIField(StringField):
    """A string instance is valid against this attribute if it is a valid
       URI, according to RFC3986."""

    def __init__(self, **kwargs):
        """TODO: to be defined1.

        """
        super(URIField, self).__init__(format="uri", **kwargs)


class ArrayField(BaseField):

    """Represents an array field in the JSON schema"""

    def __init__(self, items=None, additional_items=None, min_items=None, max_items=None,
                 unique_items=None, **kwargs):
        """TODO: to be defined1.

        :param items: TODO
        :param additional_items: TODO
        :param min_items: TODO
        :param max_items: TODO
        :param unique_items: TODO

        """
        super(ArrayField, self).__init__(**kwargs)
        self._attrs["type"] = "array"

        if items is not None:
            self._attrs["items"] = items

        if additional_items is not None:
            self._attrs["additionalItems"] = additional_items

        if min_items is not None:
            if not is_number(min_items):
                raise TypeError("min_items must be a number")
            self._attrs["minItems"] = min_items

        if max_items is not None:
            if not is_number(max_items):
                raise TypeError("max_items must be a number")
            self._attrs["maxItems"] = max_items

        if unique_items is not None:
            if not isinstance(unique_items, bool):
                raise TypeError("unique_items must be a number")
            self._attrs["uniqueItems"] = unique_items

    def render(self, schema, roles):
        ctx, deps = super(ArrayField, self).render(schema, roles)
        for itype in ("items", "additionalItems"):
            if itype not in ctx:
                continue
            if isinstance(ctx[itype], (list, tuple)):
                items = ctx[itype]
                new_items = []
                for value in items:
                    rendered, new_deps = value.render(schema, roles)
                    new_items += [rendered]
                    deps.update(new_deps)
                ctx[itype] = new_items
            else:
                ctx[itype], new_deps = ctx[itype].render(schema, roles)
                deps.update(new_deps)
        return ctx, deps


class DictField(BaseField):

    """Represents an array field in the JSON schema"""

    def __init__(self, properties=None,
                 pattern_properties=None,
                 additional_properties=None,
                 min_properties=None, max_properties=None,
                 unique_properties=None, **kwargs):
        """TODO: to be defined1.

        :param items: If items is a field or Document all elements must validate against it,
                      if items is an array each element in array must validate agains the same
                      element in the instance's array
        :param additional_items: Must be a field or document that specifies the schema of any
                                 other items
        :param min_items: minimum number of items
        :param max_items: maximum number of items
        :param unique_items: must all items be unique

        """

        super(DictField, self).__init__(**kwargs)

        self._attrs["type"] = "object"

        if properties is not None:
            if not isinstance(properties, dict):
                raise TypeError("properties must be a dict")
            self._attrs["properties"] = properties

        if pattern_properties is not None:
            if not isinstance(pattern_properties, dict):
                raise TypeError("pattern_properties must be a dict")
            self._attrs["patternProperties"] = pattern_properties

        if additional_properties is not None:
            # if not isinstance(additional_properties, dict):
            #    raise TypeError("additional_properties must be a dict")
            self._attrs["additionalProperties"] = additional_properties

        if min_properties is not None:
            if not is_number(min_properties):
                raise TypeError("min_properties must be a number")
            self._attrs["minProperties"] = min_properties

        if max_properties is not None:
            if not is_number(max_properties):
                raise TypeError("max_properties must be a number")
            self._attrs["maxProperties"] = max_properties

    def render(self, schema, roles):  # , ctx=None):
        ctx, deps = super(DictField, self).render(schema, roles)
        for ptype in ("properties", "patternProperties"):
            if ptype not in ctx:
                continue

            props = ctx[ptype]
            for name, value in six.iteritems(props):
                props[name], new_deps = value.render(schema, roles)
                deps.update(new_deps)

        if "additionalProperties" in ctx:
            if not isinstance(ctx["additionalProperties"], bool):
                add_props, new_deps = ctx["additionalProperties"].render(schema, roles)
                ctx["additionalProperties"] = add_props
                deps.update(new_deps)
        return ctx, deps


class DocumentField(BaseField):

    """Document Ref Field allows referencing subdocuments as fields of other documents"""

    def __init__(self, document, as_ref=False, **kwargs):
        """TODO: to be defined1.

        :param document: Either a string or a Document subclass
        :param as_ref: Should document be referenced inline or as a JSON pointer reference

        """
        self._document = document
        self._as_ref = as_ref
        kwargs = {}
        super(DocumentField, self).__init__(**kwargs)

    def render(self, schema, roles):
        if self._as_ref:
            ref = schema.get_ref_name(self._document)
            return {
                "$ref": ref
            }, set([ref])
        else:
            cls = schema.resolve(self._document)
            return cls.render(schema, roles)
