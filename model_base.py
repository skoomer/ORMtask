import logging
import psycopg2
from fields import Field, AutoIncrementIDField, OneToOneField
from connect_db import ConnectDB

log = logging.getLogger(__name__)


class ModelBase(type):
    manager_class = ConnectDB

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()

    def __new__(cls, name, bases, attrs, **kwargs):
        connection = ConnectDB.connection
        if name == __class__.__name__:
            return super().__new__(cls, name, bases, attrs)
        table_name = name
        model_fields = []
        new_attrs = {}

        if attrs.get("id") is None:
            new_attrs["id"] = AutoIncrementIDField()

        for key, value in attrs.items():
            new_attrs[key] = value

        for key, val in new_attrs.items():
            if isinstance(val, Field):
                model_fields.append(val)
                setattr(val, "column_name", key)

        new_attrs["connection"] = connection
        new_attrs["table_name"] = table_name
        new_attrs["fields"] = model_fields

        new_class = super().__new__(cls, name, bases, new_attrs)

        return new_class


class Model(metaclass=ModelBase):
    def __init__(self, rel_class=None, **kwargs):

        self.attrs = kwargs
        self.query = ConnectDB._get_cursor()

        for key, value in self.attrs.items():
            for column in self.find_rel_field():
                if key == column.column_name:
                    column.column = value

        for key, val in kwargs.items():
            setattr(self, key, val)

    def find_rel_field(self):

        new_obj = []

        for field in self.fields:
            if isinstance(field, OneToOneField):
                new_obj.append(field)
        return new_obj

    @classmethod
    def create_table(cls):
        """Creates the table for the model"""
        log.info(f"Creating table for Model '{cls.table_name}'")

        columns = [f"{field.column_name} {field.to_sql()}" for field in cls.fields]

        query = """
                CREATE TABLE IF NOT EXISTS %s (
                    %s
                )""" % (
            cls.table_name,
            ",\n".join(columns),
        )
        connection = cls.connection
        cursor = connection.cursor()
        cursor.execute(query)

    def save(self, commit: bool = True):
        """save current instance to table"""
        attrs = self.attrs
        ids = attrs.get("id", None)
        if ids:
            self._update()
        else:
            table_name = self.table_name
            col_string = ", ".join(attrs.keys())
            param_string = ", ".join("%s" for _ in range(len(attrs.keys())))
            query = f"INSERT INTO {table_name} ({col_string}) VALUES({param_string}) RETURNING Id;"
            values = []

            for v in attrs.values():
                if isinstance(v, Model):
                    values.append(v.id)
                else:
                    values.append(v)

            self.query.execute(query, tuple(values))

    def _update(self):
        """Updates current instance"""
        attrs = self.attrs
        ids = attrs.get("id", None)
        if ids:
            table_name = self.table_name
            new_values = ", ".join([f"{key}=%s" for key in attrs.keys()])
            query = f"UPDATE {table_name} SET {new_values} WHERE id={ids};"
            self.query.execute(query, tuple(attrs.values()))
        else:
            raise AttributeError('Instance no have ids for update')

    @classmethod
    def get(cls, ids):
        query = "SELECT * FROM {} WHERE id = {}".format(cls.table_name, ids)
        connection = cls.connection
        cursor = connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cursor.execute(query)
        new_attrs = {}
        record = cursor.fetchone()

        for field in cls.fields:
            new_attrs[field.column_name] = getattr(record, field.column_name)

            if isinstance(field, OneToOneField):

                new_attrs[field.column_name] = OneToOneField(field.to_class).get_rel_class_id()

        return cls(**new_attrs)
