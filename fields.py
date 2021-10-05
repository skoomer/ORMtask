import datetime


class Field:
    def __init__(self, unique: bool = False, name=None, column_type=None,
                 primary_key=False, default=None, value=None, null=False, blank=False):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        self.blank, self.null = blank, null
        self.value = value
        self.nullable = null
        self.is_unique = unique
        self.column_name = None

    def set_null(self, value):
        self.null = value
        if self.null is False:
            self.null = 'NOT NULL'
        else:
            self.null = 'NULL'
        return self.null

    def __str__(self):
        return "<%s, %s, %s>" % (self.__class__.__name__, self.column_type, self.name)


class VarcharField(Field):
    def __init__(
            self, name=None, null=False, primary_key=False, default=None, max_len=256, **kwargs):
        super(VarcharField, self).__init__(name, primary_key, default, **kwargs)
        self.max_len = max_len
        self.name = name
        self.field_type = 'varchar'
        self.null = null

    def __set__(self, instance, value):
        if isinstance(value, str):
            if len(value) <= self.max_len:
                self.value = value
            else:
                raise TypeError('Beyond the maximum length')
        else:
            raise TypeError('need a str')

    def to_sql(self):
        null = ""
        unique = ""
        pg_type = f"VARCHAR({self.max_len})"
        if not self.nullable:
            null = " NOT NULL"
        if self.is_unique:
            unique = " UNIQUE"
        if not self.max_len:
            pg_type = "TEXT"

        return f"{pg_type}{unique}{null}"

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__,  self.name)


class IntegerField(Field):
    def __init__(self, name=None, value=None, primary_key=False, default=0,
                 max_len=99, min_len=0, null=False, **kwargs):
        super(IntegerField, self).__init__(name, default, primary_key, default, **kwargs)
        self.max_len = max_len
        self.min_len = min_len
        self.name = name
        self.field_type = 'integer'

    def __set__(self, instance, value):
        if isinstance(value, int):
            if self.max_len <= value >= self.min_len:
                self.value = value
            else:
                raise TypeError('Beyond the maximum length')
        else:
            raise TypeError('need a int')

    def to_sql(self):
        null = ""
        unique = ""
        pg_type = "INTEGER"
        if not self.nullable:
            null = " NOT NULL"
        if self.is_unique:
            unique = " UNIQUE"
        return f"{pg_type}{unique}{null}"

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

    def to_sql(self):
        null = ""
        unique = ""
        pg_type = "TIMESTAMP"
        if not self.nullable:
            null = " NOT NULL"
        if self.is_unique:
            unique = " UNIQUE"

        if self.has_timezone:
            pg_type = "TIMESTAMP WITH TIMEZONE"

        return f"{pg_type}{unique}{null}{self._get_default_val()}"


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

    def to_sql(self):
        null = " NOT NULL"
        unique = ""

        if self.nullable:
            null = " NULL"
        if self.is_unique:
            unique = " UNIQUE"
        return f"BOOL{unique}{null}"


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
