from rest_framework import serializers

from product_manager_ices.models import Ices, Flavour


class AddIcesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ices
        fields = "__all__"



class AddFlavourSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = ("flavour",)



# class OrderListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
