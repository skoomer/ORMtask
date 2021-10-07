import datetime
from orm_task import ConnectDB
from model import Model
from fields import IntegerField, VarcharField, DateTimeField, BooleanField


class Car(Model):
    manager_class = ConnectDB
    table_name = "car"

    id = IntegerField("id", max_len=256)
    name = VarcharField(name="name", max_len=50)
    entity = IntegerField("entity", max_len=50)
    pub_date = DateTimeField(name="pub_date", auto_now_add=datetime.datetime.now())
    available = BooleanField(name="available", deffault=True)


ConnectDB.set_connection()

car = Car(id=1, entity=3, name='opel')


car = Car.objects.select('name', 'id')

print(car)
