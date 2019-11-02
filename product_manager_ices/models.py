from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from users_app.models import MyUser


class Flavour(models.Model):
    flavour = models.CharField(max_length=45)
    def __str__(self):
        return f"{self.flavour}"


class Ices(models.Model):
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"price:{self.price}, type:{self.type}"

class OrderItem(models.Model):
    ice = models.ForeignKey(Ices, on_delete=models.CASCADE)
    flavour=models.ManyToManyField(Flavour)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.ice.type} {self.ice.price}zł Flavouers:{'/'.join([str(flav) for flav in self.flavour.all()])}"

    def get_total_ice_price(self):
        return self.quantity * self.ice.price

    def get_final_price(self):
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_ice_price()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Order(models.Model):
    STATUS_CHOICE = (
        (1, 'Started'),
        (2, 'Waiting'),
        (3, 'Finished'),
    )
    worker_owner=models.ForeignKey(MyUser,on_delete=models.SET(get_sentinel_user), null=True)
    ices_ordered = models.ManyToManyField(OrderItem, related_name="order_ice")
    time_sell = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICE,default=1)

    def __str__(self):
        return f"Order content:{self.ices_ordered.all()} {self.time_sell} {self.status}"

    def get_total(self):
        total = 0
        for order_item in self.ices_ordered.all():
            total += order_item.get_final_price()
        return total
