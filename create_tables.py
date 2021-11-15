from connect_db import ConnectDB
from model import Model
from fields import IntegerField
ConnectDB.set_connection()


class Book2(Model):

    id = IntegerField(auto_increment=True)
    entity = IntegerField(min_len=3)
