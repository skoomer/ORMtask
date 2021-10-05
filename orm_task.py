import datetime
import psycopg2
import environ
from fields import VarcharField, IntegerField, BooleanField, DateTimeField
root = environ.Path(__file__)   # get root of the project
env = environ.Env()
environ.Env.read_env()


def connect_orm_task():
    return psycopg2.connect(
        dbname=env.str("POSTGRES_DB"),
        user=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("POSTGRES_HOST"),
        port=env.str("POSTGRES_PORT")
    )


def db_list_tables(conn):
    cur = conn.cursor()
    cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    return cur.fetchall()


connection = connect_orm_task()
cursor = connection.cursor()


def close_connect(conn):
    cur = conn.cursor()
    if conn:
        print("Connection close")
        cur.close()
        conn.close()
    else:
        print("Error connection close")


def create_table(
    sql_query: str,
    conn: psycopg2.extensions.connection,
    cur: psycopg2.extensions.cursor,
) -> None:
    try:
        # Execute the table creation query
        cur.execute(sql_query)
    except ValueError as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()


class Car:
    table_name = "car"

    id = IntegerField("id", max_len=256)
    name = VarcharField(name="name", max_len=50)
    entity = IntegerField("entity", max_len=50)
    pub_date = DateTimeField(name="pub_date", auto_now_add=datetime.datetime.now())
    available = BooleanField(name="available", deffault=True)


car = Car(id=1, entity=3, name='opel').create_table(connection)

if __name__ == "__main__":
    # If the modules can't be imported, the following print won't happen
    print("Successfully imported the modules!")
