from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import MultipleChoiceField

from product_manager_ices.models import Ices, Flavour, Order, OrderItem


class AddIcesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ices
        fields = "__all__"


class AddFlavourSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = ["flavour"]


class OrderListSerializer(serializers.ModelSerializer):
    orderitem=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ('worker_owner', 'time_sell', 'orderitem')


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', "worker_owner", 'time_sell', 'status', 'orderitem']

    def create(self, validated_data):
        orderitems = validated_data.pop('orderitem')
        order = Order.objects.create(**validated_data)
        order.orderitem.add(*orderitems)
        order.save()
        return order


class OrderItemCreateSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", 'quantity', 'ice', 'ice_id', 'flavour', "order"]


    def create(self, validated_data):
        flavour = validated_data.pop('flavour')
        order_ids = validated_data.pop('order')
        orderitem = OrderItem.objects.create(**validated_data)

        # validation for Thai ice to only 3 flavoures
        if (len([*flavour]) > 3) and (orderitem.ice.type == "thai"):
            raise ValidationError('Thai ice can be made only from 3 flavoures')

        # validation for scoope ice, quantity == number of flavoures(scoope)
        if orderitem.ice.type == "scoope":
            orderitem.quantity=len([*flavour])

        orderitem.flavour.add(*flavour)
        orderitem.order.add(*order_ids)
        orderitem.save()
        return orderitem
