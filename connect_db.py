import psycopg2
import environ
root = environ.Path(__file__)   # get root of the project
env = environ.Env()
environ.Env.read_env()


class ConnectDB:
    connection = None

    @classmethod
    def set_connection(cls):
        connection = psycopg2.connect(
            dbname=env.str("POSTGRES_DB"),
            user=env.str("POSTGRES_USER"),
            password=env.str("POSTGRES_PASSWORD"),
            host=env.str("POSTGRES_HOST"),
            port=env.str("POSTGRES_PORT"),
        )
        connection.autocommit = True
        cls.connection = connection

    def __init__(self, model_class, **kwargs):
        self.model_class = model_class
        self.attrs = kwargs
        self.db = getattr(model_class, "db", None)

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)


if __name__ == "__main__":
    # If the modules can't be imported, the following print won't happen
    print("Successfully imported the modules!")
