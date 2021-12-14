
from model import Model
from fields import IntegerField, AutoIncrementIDField, OneToOneField
from connect_db import ConnectDB


ConnectDB.set_connection()


class Book(Model):

    id = AutoIncrementIDField()
    entity = IntegerField()


class Author(Model):
    id = AutoIncrementIDField()
    # id = IntegerField(auto_increment=True, primary_key=True)
    entity = IntegerField()
    book_id = OneToOneField(Book)


# Book().create_table()
# Author().create_table()
# Book(entity=5).save()
# Author(entity = 33,book_id = 1).save()

class Profile(Model):
    id = AutoIncrementIDField()
    entity = IntegerField()


class MyUser(Model):
    id = AutoIncrementIDField()
    profile_id = OneToOneField(Profile)

# Profile().create_table()
# MyUser().create_table()
# Profile(entity=5).save()
# MyUser(profile_id = 1).save()


# author = Author()
# author.get(ids=1)
# print(author.entity)
