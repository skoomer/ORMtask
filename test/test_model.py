from unittest.case import TestCase
from model import Model
from fields import IntegerField
from connect_db import ConnectDB


class Book(Model):
    id = IntegerField(auto_increment=True)
    entity = IntegerField()


class TestModel(TestCase):

    def setUp(self):
        Book.create_table()
        self.cursor = ConnectDB.connection.cursor()

    def test_check_exist_table(self):
        query = "SELECT EXISTS ( SELECT * FROM information_schema.tables WHERE table_name = 'book');"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (True,))

    def test_get_fields_name(self):
        book = Book()
        self.assertEqual(getattr(book.fields[0], 'column_name'), 'id')

    def test_check_table_name(self):
        self.assertEqual(Book.__name__, 'Book')

    def test_check_class_attr_with_param(self):
        query = "select exists ( select entity from book where null is null );"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (False,))

    def test_model_save_instance(self):
        Book(entity=4).save()
        Book(entity=4).save()
        query = "SELECT count(*) FROM book;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (2,))

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
        drop = "DROP TABLE IF EXISTS book;"
        self.cursor.execute(drop)
