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
    # ices_ordered = serializers.PrimaryKeyRelatedField(many=True,required=False,queryset=OrderItem.objects.all())
    # ices_ordered = OrderItemCreateSerializer(many=True,required=False)

    class Meta:
        model = Order
        fields = ['id',"worker_owner", 'time_sell', 'status','parentorder']


    def create(self, validated_data):
        # ices_ordered = validated_data.pop('ices_ordered')
        parentorder = validated_data.pop('parentorder')
        order = Order.objects.create(**validated_data)
        order.parentorder.add(*parentorder)
        order.save()
        return order


class OrderItemCreateSerializer(serializers.ModelSerializer):
    # flavour=serializers.MultipleChoiceField(choices=[(flav.id, flav.flavour) for flav in Flavour.objects.all()])
    # flavour=AddFlavourSerializers(many=True)
    # ice=serializers.ChoiceField(choices=[(typeice.id, typeice.type) for typeice in Ices.objects.all()])
    # ice=AddIcesSerializers()
    order=serializers.PrimaryKeyRelatedField(many=True,required=True,queryset=Order.objects.all())

    class Meta:
        model = OrderItem
        fields = ["id",'quantity','ice','ice_id','flavour',"order"]

    def create(self, validated_data):
        flavour = validated_data.pop('flavour')

        orderids = validated_data.pop('order')
        orderitem = OrderItem.objects.create(**validated_data)
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