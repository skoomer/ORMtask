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

    def test_class_desc_str(self):
        desc = self._make_one_field()
        self.assertEqual(desc.__str__(), '<Field, None>')


class TestIntegerField(TestCase):

    def _make_one_integerfield(self, *args, **kw):
        from fields import IntegerField
        return IntegerField(min_len=5, max_len=8, unique=True, name='entity', auto_increment=True, *args, **kw)

    def test_class_validate_int(self):
        desc = self._make_one_integerfield()
        res = desc.validate(5)

        self.assertEqual(res, 5)

    def test_class_validate(self):
        desc = self._make_one_integerfield()
        with pytest.raises(TypeError) as excinfo:
            value = 'str'
            desc.validate(value)
        self.assertEqual(str(excinfo.value), (f'Expected {value!r} to be an int'))

        with pytest.raises(ValueError) as excinfo:
            value = 86
            desc.validate(value)
        self.assertEqual(str(excinfo.value), (f'Expected {value!r} to be no more than {desc.max_len!r}'))

        with pytest.raises(ValueError) as excinfo:
            value = 1
            desc.validate(value)
        self.assertEqual(str(excinfo.value), (f'Expected {value!r} to be at least {desc.min_len!r}'))

    def test_class_desc_get(self):
        desc = self._make_one_integerfield(value=5)
        res = desc.__get__(None, 5)
        self.assertEqual(res, 5)

    def test_class_desc_set(self):
        desc = self._make_one_integerfield()
        desc.validate(5)
        desc.__set__(desc.value, 5)
        self.assertEqual(desc.value, 5)

    def test_class_desc_str(self):
        desc = self._make_one_integerfield()
        self.assertEqual(desc.__str__(), '<IntegerField, entity>')

    def test_class_desc_to_sql(self):
        desc = self._make_one_integerfield()
        self.assertEqual(desc.to_sql(), 'SERIAL UNIQUE NOT NULL')
