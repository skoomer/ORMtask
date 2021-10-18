from unittest.case import TestCase
import psycopg2
from psycopg2 import pool
import environ
from model import Model
from fields import IntegerField
from connect_db import ConnectDB


root = environ.Path(__file__)   # get root of the project
env = environ.Env()
environ.Env.read_env()

ConnectDB.set_connection()

con = ConnectDB.connection

pool = psycopg2.pool.SimpleConnectionPool(1, 10, database=env.str("POSTGRES_DB"),
                                          user=env.str("POSTGRES_USER"),
                                          password=env.str("POSTGRES_PASSWORD"),
                                          host=env.str("POSTGRES_HOST"),
                                          port=env.str("POSTGRES_PORT"))


class Book(Model):
    manager = ConnectDB
    table_name = 'book'
    id = IntegerField(name='id', auto_increment=True)
    entity = IntegerField(name='entity')


class TestModel(TestCase):

    def setUp(self):
        self.cursor = con.cursor()
        with pool.getconn() as conn:
            Book.create_table(conn)
            pool.putconn(conn)

    def test_check_exist_table(self):
        query = "SELECT EXISTS ( SELECT * FROM information_schema.tables WHERE table_name = 'book');"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (True,))

    def test_model_save_instance(self):
        Book(entity=3).save(con)
        Book(entity=3).save(con)
        query = "SELECT count(*) FROM book;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (2,))

    def test_update_instance(self):
        book = Book(entity=1)
        book.update(con, ids=1)
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
