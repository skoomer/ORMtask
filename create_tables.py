
from model import Model
from fields import IntegerField, AutoIncrementIDField, OneToOneField
from connect_db import ConnectDB


ConnectDB.set_connection()


class Book(Model):

    id = AutoIncrementIDField()
    entity = IntegerField()
    my = IntegerField()


class Book2(Model):
    id = AutoIncrementIDField()
    entity = IntegerField()


class Author(Model):
    id = AutoIncrementIDField()
    # id = IntegerField(auto_increment=True, primary_key=True)
    entity = IntegerField()

    book_id = OneToOneField(Book)
    he = IntegerField()


# a = Author().create_table()
# a = Author(he=55,entity=33,book_id=1).save()
author = Author(book_id=1)


print(author.book_id)
