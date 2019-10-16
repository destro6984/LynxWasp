from rest_framework import serializers

<<<<<<< HEAD

from product_manager_ices.models import Ices, Flavour


=======
from product_manager_ices.models import Order, Ices, Flavour


class AddIcesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ices
        fields = "__all__"
>>>>>>> usahe drf check add falvour


class AddFlavourSerializers(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD

        model = Ices
        fields = "__all__"



class AddFlavourSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = ("flavour",)
=======
        model = Flavour
        fields = ("flavour",)


# class OrderListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
>>>>>>> usahe drf check add falvour
