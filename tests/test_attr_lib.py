from jsg import Document
from jsg.fields import NumberField, IntField, StringField, ArrayField, DictField
from utils import check_schema, schema
import pytest


def test_defaults(schema):
    @schema.add()
    class A(Document):
        a = NumberField(default=1)

    Aclass = A.get_class()
    a = Aclass()
    assert a.a == 1


def test_numfield(schema):
    @schema.add()
    class A(Document):
        a = NumberField()

    Aclass = A.get_class()
    a = Aclass(a=1)
    assert a.a == 1
    a = Aclass(a=1.1)
    assert a.a == 1.1
    with pytest.raises(TypeError):
        b = Aclass(a="a")


def test_intfield(schema):
    @schema.add()
    class A(Document):
        a = IntField()

    Aclass = A.get_class()
    a = Aclass(a=1)
    assert a.a == 1
    with pytest.raises(TypeError):
        b = Aclass(a=1.1)


def test_stringfield(schema):
    @schema.add()
    class A(Document):
        a = StringField()

    Aclass = A.get_class()
    a = Aclass(a="a")
    assert a.a == "a"
    with pytest.raises(TypeError):
        b = Aclass(a=1)


def test_arrayfield(schema):
    @schema.add()
    class A(Document):
        a = ArrayField()

    Aclass = A.get_class()
    a = Aclass(a=[1, 2, 3])
    assert a.a == [1, 2, 3]
    with pytest.raises(TypeError):
        b = Aclass(a=1)


def test_dictfield(schema):
    @schema.add()
    class A(Document):
        a = DictField()

    Aclass = A.get_class()
    a = Aclass(a={"a": 1})
    assert a.a == {"a": 1}
    with pytest.raises(TypeError):
        b = Aclass(a=1)
