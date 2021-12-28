from typing import Any, Optional
import psycopg2
import psycopg2.extras
import model_base

from connect_db import ConnectDB


class Field:
    def __init__(
        self,
        unique: bool = False,
        primary_key: bool = None,
        default: Any = None,
        value=None,
        null: bool = False,
        blank=False,
    ):
        self.primary_key = primary_key
        self.default = default
        self.blank, self.null = blank, null
        self.nullable = null
        self.is_unique = unique
        self.column_name = None

        self.value = value

    def set_null(self, value):
        self.null = value
        if self.null is False:
            self.null = "NOT NULL"
        else:
            self.null = "NULL"
        return self.null

    def _get_null_val(self):
        if self.nullable:
            return " NULL"
        elif not self.nullable:
            return " NOT NULL"

    def _get_pk_val(self):
        if self.primary_key:
            return " PRIMARY KEY"
        else:
            return ""

    def _get_unique_val(self):
        if self.is_unique:
            return " UNIQUE"
        else:
            return ""

    def is_real_type(self):
        """To check if the field is a real data type"""
        return True

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__, self.column_name)


class IntegerField(Field):
    python = int

    def __init__(
        self,
        max_len=99,
        min_len=0,
        value=None,
        primary_key: bool = None,
        unique: bool = False,
        small_int: bool = False,
        big_int: bool = False,
        auto_increment: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.primary_key = primary_key
        self.max_len = max_len
        self.min_len = min_len
        self.small_int = small_int
        self.big_int = big_int
        self.auto_increment = auto_increment
        self.value = value
        self.is_unique = unique

        if auto_increment:
            self.python = None

    def __get__(self, instance, owner):

        return self.value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected {value!r} to be an int")

        if self.min_len is not None and value < self.min_len:
            raise ValueError(f"Expected {value!r} to be at least {self.min_len!r}")
        if self.max_len is not None and value > self.max_len:
            raise ValueError(f"Expected {value!r} to be no more than {self.max_len!r}")
        return value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value

    def to_sql(self):
        pg_type = "INTEGER"

        if self.auto_increment:
            if self.big_int:
                pg_type = "BIGSERIAL"
            elif self.small_int:
                pg_type = "SMALLSERIAL"
            else:
                pg_type = "SERIAL"
        elif self.big_int:
            pg_type = "BIGINT"
        elif self.small_int:
            pg_type = "SMALLINT"

        return f"{pg_type}{self._get_pk_val()}{self._get_unique_val()}{self._get_null_val()}"

    def is_real_type(self):
        return not self.auto_increment

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__, self.column_name)


class AutoIncrementIDField(IntegerField):
    """An auto increasing id field, used as the id row for models"""

    python = None

    def __init__(self, small_int: bool = False, big_int: bool = False):
        super().__init__(
            big_int=big_int, small_int=small_int, auto_increment=True, primary_key=True
        )

    def is_real_type(self):
        return False


class OneToOneField(Field):
    def __init__(
        self, to_class, ids=None, sql_type: Optional[str] = "INTEGER", **kwargs
    ):
        super().__init__(**kwargs)
        if isinstance(to_class, model_base.ModelBase):
            self.to_class = to_class
        else:
            raise AttributeError("Attribute must be class object")

        if isinstance(ids, Field):
            self.ids = ids.column_name

        elif isinstance(ids, str):
            self.ids = ids

        self.ids = ids
        self.sql_type = sql_type

    def get_rel_class_id(self):
        new_obj = []
        execute_query = ConnectDB.connection.cursor(
            cursor_factory=psycopg2.extras.NamedTupleCursor
        )

        if self.to_class and self.ids is not None:
            query = "SELECT * FROM {} WHERE id = {} ".format(
                self.to_class.table_name, self.ids
            )
            new_attrs = {}
            execute_query.execute(query)
            record = execute_query.fetchone()

            for field in self.to_class.fields:
                new_attrs[field.column_name] = getattr(record, field.column_name)

            new_obj.append(self.to_class(**new_attrs))

            return new_obj.pop()

    def __get__(self, instance, owner):

        return self.get_rel_class_id()

    def to_sql(self):
        sql = "INTEGER NOT NULL \nREFERENCES {0.to_class.table_name} "

        return sql.format(self)

    def is_real_type(self):
        return False

    def check_value_type(self, value):

        if isinstance(value, float):
            raise ValueError("value must be int or class object")
        if isinstance(value, int) or value.isdigit():
            return True
        else:
            raise ValueError("value must be int or class object")

    def get_value_object(self, instance, value):
        execute_query = ConnectDB.connection.cursor(
            cursor_factory=psycopg2.extras.NamedTupleCursor
        )
        if isinstance(instance, model_base.Model):
            for field in instance.fields:
                if isinstance(field, OneToOneField):
                    query = "SELECT {} FROM {} ".format(
                        field.column_name, instance.table_name.lower()
                    )
                    execute_query.execute(query)
                    record = execute_query.fetchone()
                    ids = getattr(record, field.column_name)
                    return ids

    def __set__(self, instance, value):
        if isinstance(value, model_base.Model):
            self.ids = self.get_value_object(instance, value)
        elif self.check_value_type(value):
            self.ids = value
