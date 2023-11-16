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


class OrderSerializer(serializers.ModelSerializer):
    order_item = serializers.PrimaryKeyRelatedField(
        many=True, queryset=OrderItem.objects.all(), required=False
    )

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    worker_owner = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = ["status", "order_item", "worker_owner"]

    def create(self, validated_data):
        order_items = validated_data.pop("order_item", [])
        order = Order.objects.create(**validated_data)
        order.order_item.add(*order_items)
        order.save()
        return order

    def update(self, instance, validated_data):
        order_items = validated_data.pop("order_item", instance.order_item.all())
        instance.status = validated_data.get("status", instance.status)
        instance.order_item.set(order_items)
        instance.save()
        return instance


class OrderItemCreateSerializer(serializers.ModelSerializer):
    order = serializers.HyperlinkedRelatedField(
        view_name="order-manage", lookup_field="id", many=True, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "ice", "ice_id", "flavour", "order"]

    def create(self, validated_data):
        flavour = validated_data.pop("flavour")
        order_ids = validated_data.pop("order")
        order_item = OrderItem.objects.create(**validated_data)

        # validation for Thai ice to only 3 flavours
        if (len([*flavour]) > 3) and (order_item.ice.type == "thai"):
            raise ValidationError("Thai ice can be made only from 3 flavours")

        # validation for scoop ice, quantity == number of flavours(scoop)
        if order_item.ice.type == "scoop":
            order_item.quantity = len([*flavour])

        order_item.flavour.add(*flavour)
        order_item.order.add(*order_ids)
        order_item.save()
        return order_item


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
