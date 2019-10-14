from rest_framework import serializers

from product_manager_ices.models import Order, Ices


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AddIcesSerializers(serializers.ModelSerializer):
    class Meta:
        model= Ices
        fields= "__all__"
