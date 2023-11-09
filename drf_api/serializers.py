from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from product_manager_ices.models import Flavour, Ices, Order, OrderItem


class IceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ices
        fields = "__all__"

    def to_representation(self, instance):
        """
        Convert `type` to lowercase.
        """
        ret = super().to_representation(instance)
        ret["type"] = ret["type"].lower()
        return ret


class FlavourSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flavour
        fields = ["flavour"]

    def to_representation(self, instance):
        """
        Convert `flavour` to lowercase.
        """
        ret = super().to_representation(instance)
        ret["flavour"] = ret["flavour"].lower()
        return ret


class OrderListSerializer(serializers.ModelSerializer):
    orderitem = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("worker_owner", "time_sell", "orderitem")


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "worker_owner", "time_sell", "status", "orderitem"]

    def create(self, validated_data):
        orderitems = validated_data.pop("orderitem")
        order = Order.objects.create(**validated_data)
        order.orderitem.add(*orderitems)
        order.save()
        return order


class OrderItemCreateSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "ice", "ice_id", "flavour", "order"]

    def create(self, validated_data):
        flavour = validated_data.pop("flavour")
        order_ids = validated_data.pop("order")
        orderitem = OrderItem.objects.create(**validated_data)

        # validation for Thai ice to only 3 flavoures
        if (len([*flavour]) > 3) and (orderitem.ice.type == "thai"):
            raise ValidationError("Thai ice can be made only from 3 flavoures")

        # validation for scoope ice, quantity == number of flavoures(scoope)
        if orderitem.ice.type == "scoope":
            orderitem.quantity = len([*flavour])

        orderitem.flavour.add(*flavour)
        orderitem.order.add(*order_ids)
        orderitem.save()
        return orderitem


class UserSerializer(UserDetailsSerializer):
    location = serializers.CharField(
        allow_blank=True, source="profileuser.location"
    )  # noqa
    birth_date = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d", "iso-8601"],
        source="profileuser.birth_date",
    )
    email = serializers.EmailField(allow_blank=False)
    image_from_cl = serializers.ImageField(
        source="profileuser.image_from_cl", required=False
    )

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "last_name",
            "first_name",
            "location",
            "email",
            "birth_date",
            "image_from_cl",
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profileuser", {})

        location = profile_data.get("location", instance.profileuser.location)
        birth_date = profile_data.get(
            "birth_date", instance.profileuser.birth_date
        )  # noqa
        image_from_cl = profile_data.get(
            "image_from_cl", instance.profileuser.image_from_cl
        )

        instance = super(UserSerializer, self).update(instance, validated_data)
        # get and update user profile
        profile = instance.profileuser
        # if profile_data and location:
        profile.location = location
        profile.birth_date = birth_date
        profile.image_from_cl = image_from_cl
        profile.save()
        instance.save()
        return instance
