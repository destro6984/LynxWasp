from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import MultipleChoiceField

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
        read_only_fields = ('ices_ordered', 'worker_owner', 'time_sell')


class OrderItemCreateSerializer(serializers.ModelSerializer):
    # flavour=serializers.MultipleChoiceField(choices=[(flav.id, flav.flavour) for flav in Flavour.objects.all()])
    flavour=AddFlavourSerializers(many=True)
    # ice=serializers.ChoiceField(choices=[(typeice.id, typeice.type) for typeice in Ices.objects.all()])
    class Meta:
        model = OrderItem
        fields = ['ice','flavour','quantity']

    def create(self, validated_data):
        flavour = validated_data.pop('flavour')
        orderitem = OrderItem.objects.create(**validated_data)
        # for flav in flavour:
        orderitem.flavour.add(*flavour)
        orderitem.save()
        return orderitem

class OrderCreateSerializer(serializers.ModelSerializer):
    ices_ordered = OrderItemCreateSerializer(many=True,required=False)
    class Meta:
        model = Order
        fields = ["worker_owner", 'time_sell', 'status', 'ices_ordered']


    def create(self, validated_data):
        # ices_ordered = validated_data.pop('ices_ordered')
        order = Order.objects.create(**validated_data)
        # for ice in ices_ordered:
        #     # order.ices_ordered.add(ice)
        #     OrderItem.objects.create(**ices_ordered)
        return order

