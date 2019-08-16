from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from users_app.models import MyUser


class Flavour(models.Model):
    flavour = models.CharField(max_length=45)

    def __str__(self):
        return f"Flavour:{self.flavour}"

class Ices(models.Model):
    price=models.DecimalField(max_digits=5,decimal_places=2)
    type = models.CharField(max_length=50,unique=True)
    flavour_type=models.ManyToManyField(Flavour)
    def __str__(self):
        return f"price:{self.price},type:{self.type}"



class Order(models.Model):
    ice = models.ManyToManyField(Ices)
    sell_time = models.DateTimeField(auto_now_add=True)
    worker=models.ForeignKey(MyUser,on_delete=models.SET_NULL, null=True)

    def get_cart_items(self):
        return self.ice.all()

    def get_cart_total(self):
        return sum([ice.price for ice in self.ice.all()])

    def __str__(self):
        return f"sell_time:{self.sell_time}"
