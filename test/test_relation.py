from unittest.case import TestCase
import pytest
from model_base import Model, ModelBase
from fields import IntegerField, OneToOneField, AutoIncrementIDField
from connect_db import ConnectDB

ConnectDB.set_connection()


class Profile(Model):
    id = AutoIncrementIDField()
    entity = IntegerField()


class MyUser(Model):
    id = AutoIncrementIDField()
    profile_id = OneToOneField(Profile)


class Test_OneToOne(TestCase):
    def setUp(self):
        Profile().create_table()
        MyUser().create_table()
        self.cursor = ConnectDB._get_cursor()
        self.user = MyUser()

    def test_check_exists_relation(self):
        query = "SELECT TRUE AS EXISTS \
          FROM information_schema.columns WHERE table_name='user' and column_name= 'profile_id';"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (True,))

    def test_attr_to_class_object(self):
        desc = OneToOneField(Profile)
        check_class = isinstance(desc.to_class, ModelBase)
        self.assertEqual(check_class, True)

    def test_attr_to_class_raise(self):
        with pytest.raises(AttributeError) as er:
            OneToOneField("Profile")
        self.assertEqual(str(er.value), "Attribute must be class object")

    def test_field_column_name(self):
        for column in self.user.fields:
            if column.column_name == "profile_id":
                self.assertEqual(column.column_name, "profile_id")

    def test_check_column_none(self):
        desc = OneToOneField(Profile)
        self.assertEqual(desc.ids, None)

    def test_get_rel_class_id_is_none(self):
        desc = OneToOneField(Profile)
        self.assertEqual(desc.get_rel_class_id(), None)

    def test_get_rel_class_id(self):
        Profile(entity=5).save()
        MyUser(profile_id=1).save()
        desc = OneToOneField(Profile, ids=1).get_rel_class_id()
        self.assertEqual(desc.id, 1)

    def test_set_(self):
        with pytest.raises(ValueError) as er:
            self.user.profile_id = "test"
        self.assertEqual(str(er.value), "value must be number type")
        with pytest.raises(ValueError) as er:
            self.user.profile_id = 1.2
        self.assertEqual(str(er.value), "value must be number type")

    def tearDown(self):
        drop = "DROP TABLE IF EXISTS profile CASCADE;"
        self.cursor.execute(drop)
