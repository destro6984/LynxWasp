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






class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id',"worker_owner", 'time_sell', 'status','orderitem']


    def create(self, validated_data):
        orderitems = validated_data.pop('orderitem')
        order = Order.objects.create(**validated_data)
        order.orderitem.add(*orderitems)
        order.save()
        return order


class OrderItemCreateSerializer(serializers.ModelSerializer):
    order=serializers.PrimaryKeyRelatedField(many=True,required=True,queryset=Order.objects.all())

    class Meta:
        model = OrderItem
        fields = ["id",'quantity','ice','ice_id','flavour',"order"]

    def create(self, validated_data):
        flavour = validated_data.pop('flavour')
        orderids = validated_data.pop('order')
        orderitem = OrderItem.objects.create(**validated_data)
        # orderitem,created = OrderItem.objects.get_or_create(**validated_data)

        orderitem.flavour.add(*flavour)
        orderitem.order.add(*orderids)
        orderitem.save()
        return orderitem






# {
#         "id": 107,
#         "worker_owner": 2,
#         "time_sell": "2019-11-02T15:23:11.647027+01:00",
#         "status": 3,
#         "ices_ordered": [
#             {
#                 "id": 11,
#                 "quantity": 2,
#                 "ice": 1,
#                 "ice_id": 1,
#                 "flavour": [
#                     1,
#                     2
#                 ],
#                 "order_ice": [
#                     107
#                 ]
#             }
#         ]
#     },