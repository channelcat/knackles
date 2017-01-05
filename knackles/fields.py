from .util import Undefined

class Field:
    def __init__(self, size=None, name=None, null=False, default=Undefined):
        self.size = size
        self.name = name
        self.null = null
        self.default = default
        self.model_field_name = None

class IntegerField(Field):
    # TODO: this field
    pass

class BigInteger(IntegerField):
    # TODO: this field
    pass

class BigInteger(IntegerField):
    # TODO: this field
    pass

class SmallInteger(IntegerField):
    # TODO: this field
    pass

class IDField(IntegerField):
    # TODO: this field
    pass

class FloatField(Field):
    # TODO: this field
    pass

class DoubleField(FloatField):
    # TODO: this field
    pass

class DecimalField(Field):
    # TODO: this field
    pass

class CharField(Field):
    # TODO: this field
    pass

class FixedChar(CharField):
    # TODO: this field
    pass

class TextField(Field):
    # TODO: this field
    pass

class BlobField(Field):
    # TODO: this field
    pass

class UUIDField(Field):
    # TODO: this field
    pass

class DateTimeField(Field):
    # TODO: this field
    pass

class DateField(Field):
    # TODO: this field
    pass

class TimeField(Field):
    # TODO: this field
    pass

class TimestampField(IntegerField):
    # TODO: this field
    pass

class BooleanField(Field):
    # TODO: this field
    pass

class ForeignKeyField(IntegerField):
    # TODO: this field
    pass

class CompositeKeyField(object):
    """A primary key composed of multiple columns."""
    # TODO: this field
    pass