from typing import Any


class Field:
    def __init__(
        self,
        unique: bool = False,
        primary_key=False,
        name=None,
        column_type=None,
        default: Any = None,
        value=None,
        null: bool = False,
        blank=False
    ):
        self.primary_key = primary_key
        self.default = default
        self.blank, self.null = blank, null
        self.nullable = null
        self.is_unique = unique
        self.column_name = None
        self.name = name
        self.value = value

    def set_null(self, value):
        self.null = value
        if self.null is False:
            self.null = 'NOT NULL'
        else:
            self.null = 'NULL'
        return self.null

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__, self.column_name)


class IntegerField(Field):
    python = int

    def __init__(
            self,
            max_len=99,
            min_len=0,
            value=None,
            unique: bool = False,
            small_int: bool = False,
            big_int: bool = False,
            auto_increment: bool = False,
            **kwargs):
        super().__init__(**kwargs)
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
            raise TypeError(f'Expected {value!r} to be an int')

        if self.min_len is not None and value < self.min_len:
            raise ValueError(
                f'Expected {value!r} to be at least {self.min_len!r}'
            )
        if self.max_len is not None and value > self.max_len:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.max_len!r}'
            )
        return value

    def __set__(self, instance, value):
        if self.validate(value):
            self.value = value

    def to_sql(self):
        null = ""
        unique = ""
        pg_type = "INTEGER"
        if not self.nullable:
            null = " NOT NULL"
        if self.is_unique:
            unique = " UNIQUE"

        if self.auto_increment:
            if self.big_int:
                pg_type = "BIGSERIAL"
            elif self.small_int:
                pg_type = "SMALLSERIAL"
            pg_type = "SERIAL"

        return f"{pg_type}{unique}{null}"

    def __str__(self):
        return "<%s, %s>" % (self.__class__.__name__, self.name)
