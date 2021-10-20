from connect_db import ConnectDB
from model import Model
from fields import IntegerField
ConnectDB.set_connection()
conn = ConnectDB.connection


class Book(Model):
    manager_class = ConnectDB
    __tablename__ = "book"
    id = IntegerField(name="id", auto_increment=True, unique=True)
    entity = IntegerField(name="entity", min_len=3)
