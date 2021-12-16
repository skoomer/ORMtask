import psycopg2
import environ

root = environ.Path(__file__)  # get root of the project
env = environ.Env()
environ.Env.read_env()


class ConnectDB:
    connection = None
    dbname = env.str("POSTGRES_DB")
    user = env.str("POSTGRES_USER")
    password = env.str("POSTGRES_PASSWORD")
    host = 4333
    port = env.str("POSTGRES_PORT")

    @classmethod
    def set_connection(cls):
        try:
            connection = psycopg2.connect(
                dbname=cls.dbname,
                user=cls.user,
                password=cls.password,
                host=cls.host,
                port=cls.port,
            )
            connection.autocommit = True
            cls.connection = connection
        except psycopg2.OperationalError as ex:
            raise ConnectionError(
                "Unable connect database check run server and port host etc ...."
            ) from ex
        return cls.connection

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
