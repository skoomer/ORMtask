from connect_db import ConnectDB
from model import Model
from fields import IntegerField
ConnectDB.set_connection()
conn = ConnectDB.connection


class Book3(Model):

    id = IntegerField(name="id", auto_increment=True, unique=True)
    entity = IntegerField(name="entity", min_len=3)
