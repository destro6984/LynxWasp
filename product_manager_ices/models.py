from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from users_app.models import MyUser


class Flavour(models.Model):
    flavour = models.CharField(max_length=45)
    def __str__(self):
        return f"Flavour:{self.flavour}"

class Ices(models.Model):
    type = models.CharField(max_length=50)
    # price=models.ForeignKey(Price,on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    flavour_type=models.ManyToManyField(Flavour)
    def __str__(self):
        return f"price:{self.price}, type:{self.type},Flavour:{self.flavour_type}"


class OrderItem(models.Model):
    # worker = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    # ordered = models.BooleanField(default=False)
    ice = models.ForeignKey(Ices, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.ice.type}"

    def get_total_ice_price(self):
        return self.quantity * self.ice.price

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()
    def get_final_price(self):
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_ice_price()

class Order(models.Model):
    # worker = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    # ref_code = models.CharField(max_length=20, blank=True, null=True)
    ices_ordered = models.ManyToManyField(OrderItem)
    time_sell = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField()
    # ordered = models.BooleanField(default=False)
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
        return f"{self.ices_ordered}   {self.time_sell}"

    def get_total(self):
        total = 0
        for order_item in self.ices_ordered.all():
            total += order_item.get_final_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


















class Order(models.Model):
    ice = models.ManyToManyField(Ices)
    sell_time = models.DateTimeField(auto_now_add=True)
    # worker=models.ForeignKey(MyUser,on_delete=models.SET_NULL, null=True)

    def get_cart_items(self):
        return self.ice.all()

    def get_cart_total(self):
        return sum([ice.price for ice in self.ice.all()])

    def __str__(self):
        return f"sell_time:{self.sell_time}"