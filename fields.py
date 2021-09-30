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
        self, name=None, value=None, primary_key=False, field_type='varchar', default=None, ddl="varchar(100)", max_len=256
    ):
        super(VarcharField, self).__init__(name, ddl, primary_key, default)
        self.max_len = max_len
        self.name = name
        self.field_type = 'VARCHAR'

    def __set__(self, instance, value):
      if isinstance(value, str):
        if len(value) <= self.max_len:
          self.value = value
        else:
          raise TypeError('Beyond the maximum length')
      else:
        raise TypeError('need a str')

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__,  self.name)


class IntegerField(Field):
    def __init__(self, name=None, value=None, primary_key=False, default=0, max_len=99, min_len=0):
        super(IntegerField, self).__init__(name, default, primary_key, default)
        self.max_len = max_len
        self.min_len = min_len
        self.name = name
        self.field_type = 'integer'

    def __set__(self, instance, value):
      if isinstance(value, int):
        if value <= self.max_len and value >= self.min_len:
          self.value = value
        else:
          raise TypeError('Beyond the maximum length')
      else:
        raise TypeError('need a int')

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__,  self.name)


class DateTimeField(Field):
 
    python = datetime

    def __init__(self, auto_now_add: bool = False, has_timezone: bool = False, name=None, **kwargs):
        super(DateTimeField, self).__init__(name=name, column_type=None, primary_key=False, default=datetime, **kwargs)
        self.automatically_add = auto_now_add
        self.has_timezone = has_timezone
        self.field_type = 'timestamp'

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
        self.field_type = 'boolean'

    def __set__(self, instance, value):
        if isinstance(value, bool):
            self.value = value
        else:
            raise TypeError("need a bool")


class OneToOneField(Field):
    def __init__(self, name=None, rel_class=None):
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
