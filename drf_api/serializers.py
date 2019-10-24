from django.utils import timezone
from rest_framework import serializers

from product_manager_ices.models import Ices, Flavour, Order, OrderItem


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


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    ices_ordered=OrderItemCreateSerializer(many=True)
    class Meta:
        model= Order
        fields=["worker_owner",'time_sell','status','ices_ordered']

    def create(self, validated_data):
        ices_ordered = validated_data.pop('ices_ordered')
        order = Order.objects.create( **validated_data)
        for ices in ices_ordered:
            OrderItem.objects.create( **ices_ordered)
        return order