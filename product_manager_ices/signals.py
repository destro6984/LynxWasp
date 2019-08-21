
from django.db.models.signals import post_save
from .models import MyUser, OrderItem, Order
from django.dispatch import receiver


@receiver(post_save, sender=OrderItem)
def create_orderitem(sender, instance, created, **kwargs):
    if created:
        ord=Order.objects.create()
        ord.ices_ordered.set(instance)


# @receiver(post_save, sender=Order)
# def save_order(sender, instance, **kwargs):
#     instance.icex_ordered.set()