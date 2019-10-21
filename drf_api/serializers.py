from rest_framework import serializers

<<<<<<< HEAD
<<<<<<< HEAD
=======
from product_manager_ices.models import Order, Ices, Flavour
>>>>>>> 99a397cf8c0d34db95c537a6cf444b4c7d5fa1ad

from product_manager_ices.models import Ices, Flavour


=======
from product_manager_ices.models import Order, Ices, Flavour

<<<<<<< HEAD
=======
class AddIcesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ices
        fields = "__all__"
>>>>>>> 99a397cf8c0d34db95c537a6cf444b4c7d5fa1ad


class AddFlavourSerializers(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
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
=======
>>>>>>> 99a397cf8c0d34db95c537a6cf444b4c7d5fa1ad
        model = Flavour
        fields = ("flavour",)


# class OrderListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
<<<<<<< HEAD
>>>>>>> usahe drf check add falvour
=======
>>>>>>> 99a397cf8c0d34db95c537a6cf444b4c7d5fa1ad
