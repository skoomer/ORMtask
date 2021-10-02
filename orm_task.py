from fields import *
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import environ
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

def close_connect(connection):
    cursor = connection.cursor()
    if connection:
        print("Connection close")
        cursor.close()
        connection.close()
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
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        print(f"Query: {cur.query}")
        conn.rollback()
        cur.close()
    else:
        # To take effect, changes need be committed to the database
        conn.commit()


class Car(object):
    table_name = "car"

    id = IntegerField("id", max_len=256)
    name = VarcharField(name="name", max_len=50)
    entity = IntegerField("entity", max_len=50)
    pub_date = DateTimeField(name="pub_date", auto_now_add=datetime.datetime.now())
    check = BooleanField(name="check", deffault=True)


sql = f"""
        CREATE TABLE {Car.table_name} (
            {Car.id.name} SERIAL PRIMARY KEY,
            {Car.name.name} {Car.name.field_type}(30),
            {Car.pub_date.name} {Car.pub_date.field_type},
            {Car.entity.name} {Car.entity.field_type},
            {Car.check.name} {Car.check.field_type}
        );
          """


create_table(sql, connection, cursor)
connection.close()
cursor.close()

if __name__ == "__main__":
    # If the modules can't be imported, the following print won't happen
    print("Successfully imported the modules!")
