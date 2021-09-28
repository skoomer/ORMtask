import psycopg2
import environ

root = environ.Path(__file__)   # get root of the project
env = environ.Env()
environ.Env.read_env()

def connect_orm_task():
  return psycopg2.connect(
    dbname = env.str("POSTGRES_DB"),
    user = env.str("POSTGRES_USER"),
    password = env.str("POSTGRES_PASSWORD"),
    host= env.str("POSTGRES_HOST"),
    port= env.str("POSTGRES_PORT")
  )

def db_list_tables(conn):
  cur = conn.cursor()
  cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
  return cur.fetchall()

a = db_list_tables(connect_orm_task())


print(a)

if __name__ == "__main__":
    # If the modules can't be imported, the following print won't happen
    print("Successfully imported the modules!")
