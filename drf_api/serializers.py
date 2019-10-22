from django.utils import timezone
from rest_framework import serializers

from product_manager_ices.models import Ices, Flavour, Order


class AddIcesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ices
        fields = "__all__"



class AddFlavourSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = ("flavour",)



class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields=('ices_ordered','worker_owner','time_sell')


