from datetime import *


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return "<%s, %s, %s>" % (self.__class__.__name__, self.column_type, self.name)


class VarcharField(Field):
    def __init__(
        self, name=None, primary_key=False, default=None, ddl="varchar(100)", max_len=4
    ):
        super(VarcharField, self).__init__(name, ddl, primary_key, default)
        self.max_len = max_len

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__,  self.name)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0, max_len=20, min_len=0):
        super(IntegerField, self).__init__(name, "bigint", primary_key, default)
        self.max_len = max_len
        self.min_len = min_len


class DateTimeField(Field):

    def __init__(self, auto_now_add: bool = False, has_timezone: bool = False, name=None, **kwargs):
        super(DateTimeField, self).__init__(name=name, column_type=None, primary_key=False, default=datetime, **kwargs)
        self.automatically_add = auto_now_add
        self.has_timezone = has_timezone

    def _get_default_val(self):
        default = ""
        if self.automatically_add:
            default = self.default or (
                " DEFAULT current_timestamp" if self.automatically_add else ""
            )
            return default
        elif self.default:
            default = self.default or (
                " DEFAULT current_timestamp" if self.automatically_add else ""
            )
            return default


class BooleanField(Field):
    def __init__(self, name=None, deffault=False):
        super(BooleanField, self).__init__(name, primary_key=False, column_type=bool, default=False)
        self.value = deffault

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if isinstance(value, bool):
            #  Judgment type
            self.value = value
        else:
            raise TypeError("need a bool")


class OneToOneField(Field):
    def __init__(self, rel_class, name=None):
        super(OneToOneField, self).__init__(
            name, primary_key=False, default=0, column_type=None
        )
        self.rel_class = rel_class

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__,  self.name)


class ForeignKey(Field):
    def __init__(self, model_class, name=None):
        super(ForeignKey, self).__init__(
            name, primary_key=False, default=0, column_type=None
        )
        self.column_type = "foreignkey"
        self.field_level = 1
        self.name = name
        self.model_class = model_class

    def field_sql(self, field_name):
        foreign_to = self.model_class.__name__.lower()
        return '"%s" integer NULL REFERENCES "%s" ("id")' % (field_name, foreign_to)
