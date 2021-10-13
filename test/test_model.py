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

    entity = IntegerField(name='entity')


class TestModel(TestCase):

    def test_create_table(self):
        with pool.getconn() as conn:
            Book.create_table(conn)
            pool.putconn(conn)

    def test_model_save(self):
        Book(entity=40).save(con)
