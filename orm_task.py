import datetime
import psycopg2
import environ
from fields import VarcharField, IntegerField, BooleanField, DateTimeField
root = environ.Path(__file__)   # get root of the project
env = environ.Env()
environ.Env.read_env()


class ConnectDB:
    connection = None

    @classmethod
    def set_connection(cls, database_settings):
        connection = psycopg2.connect(**database_settings)
        connection.autocommit = True
        cls.connection = connection

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)


class Car:
    table_name = "car"

    id = IntegerField("id", max_len=256)
    name = VarcharField(name="name", max_len=50)
    entity = IntegerField("entity", max_len=50)
    pub_date = DateTimeField(name="pub_date", auto_now_add=datetime.datetime.now())
    available = BooleanField(name="available", deffault=True)


DB_SETTINGS = {
    'host': env.str("POSTGRES_HOST"),
    'port': env.str("POSTGRES_PORT"),
    'database': env.str("POSTGRES_DB"),
    'user': env.str("POSTGRES_USER"),
    'password': env.str("POSTGRES_PASSWORD")
}

ConnectDB.set_connection(database_settings=DB_SETTINGS)

car = Car(id=1, entity=3, name='opel')

if __name__ == "__main__":
    # If the modules can't be imported, the following print won't happen
    print("Successfully imported the modules!")
