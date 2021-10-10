import logging
from fields import Field
from orm_task import ConnectDB

log = logging.getLogger(__name__)


class ModelBase(type):
    manager_class = ConnectDB

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()

    def __new__(cls, name, bases, attrs, **kwargs):
        model_fields = []
        table_name = attrs.get("__tablename__", name)
        new_attrs = {}

        for key, value in attrs.items():
            new_attrs[key] = value

        for key, val in new_attrs.items():
            if isinstance(val, Field):
                model_fields.append(val)
                setattr(val, "column_name", key)

        new_attrs["table_name"] = table_name
        new_attrs["fields"] = model_fields
        new_attrs["_valid_fields"] = [field.column_name for field in model_fields]

        new_class = super().__new__(cls, name, bases, new_attrs)

        return new_class


class Model(metaclass=ModelBase):

    def __init__(self, **kwargs):
        self.attrs = kwargs

        for key, val in kwargs.items():
            if key not in self._valid_fields:
                raise ValueError(f"error key{key}, error valid fields{self._valid_fields}")

            setattr(self, key, val)

    @classmethod
    def create_table(cls, conn):
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

        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()

    def save(self, conn, commit: bool = True):
        """Saves the current model instace to the database"""
        attrs = self.attrs
        table_name = self.table_name
        col_string = ", ".join(attrs.keys())
        param_string = ", ".join("%s" for _ in range(len(attrs.keys())))

        query = f"INSERT INTO {table_name} ({col_string}) VALUES({param_string})"
        values = []

        for v in attrs.values():
            if isinstance(v, Model):
                values.append(v.id)
            else:
                values.append(v)

        with conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            conn.commit()
