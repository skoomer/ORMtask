from unittest.case import TestCase
from model_base import Model
from fields import IntegerField, AutoIncrementIDField, OneToOneField
from connect_db import ConnectDB

ConnectDB.set_connection()


class Book(Model):
    id = AutoIncrementIDField()
    entity = IntegerField()


class Author(Model):
    id = AutoIncrementIDField()
    book = OneToOneField(Book)


class TestModel(TestCase):
    def setUp(self):
        Book().create_table()
        self.cursor = ConnectDB._get_cursor()

    def test_find_relation_field(self):
        author = Author()
        self.assertEqual(type(author.find_rel_field()[0]), OneToOneField)

    def test_create_optional_attr_if_field_have_relation_field(self):
        author = Author()
        optional_field = hasattr(author, "book_id")
        self.assertEqual(optional_field, True)

    def test_create_optional_attr_if_field_no_relation_field(self):
        author = Author()
        optional_field = hasattr(author, "avatar_id")
        self.assertEqual(optional_field, False)

    def test_check_exist_table(self):
        query = "SELECT EXISTS ( SELECT * FROM information_schema.tables WHERE table_name = 'book');"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (True,))

    def test_get_fields_name(self):
        book = Book()
        self.assertEqual(getattr(book.fields[0], "column_name"), "id")

    def test_check_table_name(self):
        self.assertEqual(Book.__name__, "Book")

    def test_check_class_attr_with_param(self):

        query = "select exists ( select entity from book where null is null );"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (False,))

    def test_model_save_instance(self):
        Book(entity=4).save()
        query = "SELECT count(*) FROM book;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (1,))

    def test_get_object(self):
        Book(entity=4).save()
        book = Book()
        book.get(ids=1)
        self.assertEqual(book.id, 1)

    def test_update_instance(self):
        Book(entity=1, id=1)._update()
        query = "SELECT book.entity FROM book WHERE id=1;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, [(1)])

    def test_check_columns(self):
        query = "SELECT TRUE AS EXISTS FROM information_schema.columns WHERE table_name='book';"
        self.cursor.execute(query)
        for column in self.cursor:
            self.assertEqual(column, (True,))

    def tearDown(self):
        drop = "DROP TABLE IF EXISTS book,author CASCADE;"
        self.cursor.execute(drop)
