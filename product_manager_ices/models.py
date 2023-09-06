from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from users_app.models import User


class Flavour(models.Model):
    flavour = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.flavour}"


class Ices(models.Model):
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"price:{self.price}, type:{self.type}"


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username="deleted")[0]


class Order(models.Model):
    class Status(models.IntegerChoices):
        STARTED = 1, "Started"
        WAITING = 2, "Waiting"
        FINISHED = 3, "Finished"

    worker_owner = models.ForeignKey(
        User, on_delete=models.SET(get_sentinel_user), null=True
    )
    time_sell = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status.choices, default=Status.STARTED)

    def __str__(self):
        return f"User:{self.worker_owner} sell-time: {self.time_sell} status: {self.get_status_display()}"

    def get_total(self):
        total = 0
        for order_item in self.orderitem.all():
            total += order_item.get_final_price()
        return total


class OrderItem(models.Model):
    ice = models.ForeignKey(Ices, on_delete=models.CASCADE)
    flavour = models.ManyToManyField(Flavour)
    quantity = models.IntegerField(default=1)
    order = models.ManyToManyField(Order, related_name="orderitem")

    def __str__(self):
        return (
            f"{self.quantity} of {self.ice.type} {self.ice.price}zł "
            f"Flavours:{'/'.join([str(flav) for flav in self.flavour.all()])}"
        )

    def get_total_ice_price(self):
        return Decimal(self.quantity) * self.ice.price

    def get_final_price(self):
        # todo
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_ice_price()
