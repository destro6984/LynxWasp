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

class Order(models.Model):
    STATUS_CHOICE = (
        (1, 'Started'),
        (2, 'Waiting'),
        (3, 'Finished'),
    )
    # ref_code = models.CharField(max_length=20, blank=True, null=True)
    worker_owner=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    ices_ordered = models.ManyToManyField(OrderItem)
    time_sell = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField()
    status = models.CharField(max_length=9, choices=STATUS_CHOICE,default=1)

    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Order content:{self.ices_ordered.all()} {self.time_sell} {self.status}"

    def get_total(self):
        total = 0
        for order_item in self.ices_ordered.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
