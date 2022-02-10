from unittest.case import TestCase
import pytest
from model_base import Model, ModelBase
from fields import OneToOneField, AutoIncrementIDField

from connect_db import ConnectDB

ConnectDB.set_connection()


class Profile(Model):
    id = AutoIncrementIDField()


class Avatar(Model):
    id = AutoIncrementIDField()


class MyUser(Model):
    id = AutoIncrementIDField()
    profile = OneToOneField(Profile)


class Test_OneToOne(TestCase):
    def setUp(self):
        Profile().create_table()
        Avatar().create_table()
        MyUser().create_table()
        self.cursor = ConnectDB._get_cursor()
        self.profile = Profile()
        self.user = MyUser()

    def test_check_exists_relation(self):
        query = "SELECT TRUE AS EXISTS \
          FROM information_schema.columns WHERE table_name='user' and column_name= 'profile';"
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
            if column.column_name == "profile":
                self.assertEqual(column.column_name, "profile")

    def test_check_column_none(self):
        desc = OneToOneField(Profile)
        self.assertEqual(desc.ids, None)

    def test_get_rel_object_is_none(self):
        desc = OneToOneField(Profile)
        self.assertEqual(desc.get_rel_object(), None)

    def test_SET_value_object_if_type_model(self):
        profile = Profile()
        user = MyUser()
        user.profile = profile
        self.assertEqual(user.profile, profile)

    def test_optional_attr_set_value_id(self):
        profile = Profile()
        profile.id = 1
        profile.save()
        profile_db = Profile.get(ids=1)
        user = MyUser()
        user.profile = profile_db
        self.assertEqual(user.profile_id, profile_db.id)

    def test_get_object_from_db(self):
        profile = Profile()
        profile.id = 1
        profile.save()
        profile_db = Profile.get(ids=1)
        user = MyUser()
        user.profile = profile_db
        user.save()
        user_db = MyUser.get(ids=1)
        self.assertEqual(user_db.profile.id, profile_db.id)

    def test_set_value_object_raises(self):
        avatar = Avatar()
        with pytest.raises(ValueError) as er:
            self.user.profile = avatar
        self.assertEqual(str(er.value), "value its not specific class")

    def test_set_(self):
        with pytest.raises(ValueError) as er:
            self.user.profile = "test"
        self.assertEqual(str(er.value), "value must be class object")

    def tearDown(self):
        drop = "DROP TABLE IF EXISTS myuser, profile CASCADE;"
        self.cursor.execute(drop)
