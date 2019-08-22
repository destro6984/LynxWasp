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
    # worker = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    # ordered = models.BooleanField(default=False)
    ice = models.ForeignKey(Ices, on_delete=models.CASCADE)
    flavour=models.ManyToManyField(Flavour)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.ice.type} Flavouers:{'/'.join([str(flav) for flav in self.flavour.all()])}"

    def get_total_ice_price(self):
        return self.quantity * self.ice.price

    def get_final_price(self):
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_ice_price()

class Order(models.Model):
    # worker = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    # ref_code = models.CharField(max_length=20, blank=True, null=True)
    worker_owner=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    ices_ordered = models.ForeignKey(OrderItem,on_delete=models.CASCADE)
    time_sell = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField()
    finished = models.BooleanField(default=False)
    # shipping_address = models.ForeignKey(
    #     'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    # billing_address = models.ForeignKey(
    #     'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    # coupon = models.ForeignKey(
    #     'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    # being_delivered = models.BooleanField(default=False)
    # received = models.BooleanField(default=False)
    # refund_requested = models.BooleanField(default=False)
    # refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        # return f"Order:{'/'.join([str(ic) for ic in self.ices_ordered.all()])}   {self.time_sell}"
        return f"Order:{self.ices_ordered.ice.type}   {'/'.join([str(ic) for ic in self.ices_ordered.flavour.all()])}  {self.time_sell}"

    def get_total(self):
        total = 0
        for order_item in self.ices_ordered.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
