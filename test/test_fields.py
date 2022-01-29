from unittest.case import TestCase
import pytest


class TestField(TestCase):

    def _make_one_field(self, *args, **kw):
        from fields import Field
        return Field(*args, **kw)

    def test_set_null(self):
        desc = self._make_one_field()
        self.assertEqual(desc.set_null(False), 'NOT NULL')
        self.assertEqual(desc.set_null(True), 'NULL')
        self.assertEqual(desc.is_real_type(), True)
        desc.nullable = True
        self.assertEqual(desc._get_null_val(), ' NULL')

    def test_class_desc_str(self):
        desc = self._make_one_field()
        self.assertEqual(desc.__str__(), '<Field, None>')


class TestIntegerField(TestCase):

    def _make_one_integerfield(self, *args, **kw):
        from fields import IntegerField
        return IntegerField(min_len=5, max_len=8, unique=True, *args, **kw)

    def setUp(self) -> None:
        self.desc = self._make_one_integerfield()

    def test_class_validate_int(self):
        res = self.desc.validate(5)
        self.assertEqual(res, 5)

    def test_class_validate(self):
        with pytest.raises(TypeError) as excinfo:
            value = 'str'
            self.desc.validate(value)
        self.assertEqual(str(excinfo.value), (f'Expected {value!r} to be an int'))

        with pytest.raises(ValueError) as excinfo:
            value = 86
            self.desc.validate(value)
        self.assertEqual(str(excinfo.value), (f'Expected {value!r} to be no more than {self.desc.max_len!r}'))

        with pytest.raises(ValueError) as excinfo:
            value = 1
            self.desc.validate(value)
        self.assertEqual(str(excinfo.value), (f'Expected {value!r} to be at least {self.desc.min_len!r}'))

    def test_class_desc_get(self):
        desc = self._make_one_integerfield(value=5)
        res = desc.__get__(None, 5)
        self.assertEqual(res, 5)

    def test_class_desc_set(self):
        self.desc.validate(5)
        self.desc.__set__(self.desc.value, 5)
        self.assertEqual(self.desc.value, 5)

    def test_class_desc_str(self):
        self.assertEqual(self.desc.__str__(), '<IntegerField, None>')

    def test_class_desc_to_sql_auto_increment_true(self):
        big_int = self._make_one_integerfield(big_int=True, auto_increment=True)
        small_int = self._make_one_integerfield(small_int=True, auto_increment=True)
        self.assertEqual(big_int.to_sql(), 'BIGSERIAL UNIQUE NOT NULL')
        self.assertEqual(small_int.to_sql(), 'SMALLSERIAL UNIQUE NOT NULL')

    def test_class_desc_to_sql_auto_increment_false(self):

        big_int = self._make_one_integerfield(big_int=True, auto_increment=False)
        small_int = self._make_one_integerfield(small_int=True, auto_increment=False)
        auto_in = self._make_one_integerfield(auto_increment=True)
        self.assertEqual(auto_in.to_sql(), 'SERIAL UNIQUE NOT NULL')
        self.assertEqual(big_int.to_sql(), 'BIGINT UNIQUE NOT NULL')
        self.assertEqual(small_int.to_sql(), 'SMALLINT UNIQUE NOT NULL')

    def test_is_real_type(self):
        real_type = self._make_one_integerfield(auto_increment=True)
        self.assertEqual(real_type.is_real_type(), False)
