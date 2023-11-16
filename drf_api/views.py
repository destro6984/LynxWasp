from django.db.models import Q
from rest_framework import filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from drf_api.serializers import (
    FlavourSerializers,
    IceSerializers,
    OrderCreateUpdateSerializer,
    OrderItemCreateSerializer,
    OrderSerializer,
    UserSerializer,
)
from product_manager_ices.models import Flavour, Ices, Order, OrderItem
from users_app.models import User


class IcesListCreateAPIView(ListCreateAPIView):
    """
    endpoint for adding types of ice
    """

    permission_classes = [IsAdminUser]
    serializer_class = IceSerializers
    queryset = Ices.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission() for permission in self.permission_classes]
        return [IsAuthenticated()]


class FlavourListCreateAPIView(ListCreateAPIView):
    """
    endpoint for adding flavours
    """

    serializer_class = FlavourSerializers
    queryset = Flavour.objects.all()


class OrdersListCreateAPIView(ListCreateAPIView):
    """
    List of Orders/Create;Update Order
    Input:
    {
        "status": null,
        "order_item": []
    }
    """

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderSerializer
        return OrderCreateUpdateSerializer

    # Order only for owner of order/ simple search of order
    def get_queryset(self):
        search = self.request.query_params.get("q", None)
        if search is not None:
            queryset = (
                Order.objects.filter(
                    Q(worker_owner__username__icontains=search)
                    | Q(time_sell__icontains=search)
                    | Q(order_item__flavour__flavour__icontains=search)
                    | Q(order_item__ice__type__contains=search)
                )
                .order_by("-time_sell")
                .distinct()
            )
        else:
            queryset = Order.objects.filter(worker_owner=self.request.user).order_by(
                "-time_sell"
            )
        return queryset

    def perform_create(self, serializer):
        open_order = Order.objects.filter(
            worker_owner=self.request.user, status=Order.Status.STARTED
        )
        # limitation if there is opened order
        if open_order:
            raise ValidationError(
                "You have already open order, please close it to open new one"
            )
        serializer.save(status=Order.Status.STARTED, worker_owner=self.request.user)


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    output:
    {
        "status": 3,
        "order_item": [
            7,
            3
        ],
        "worker_owner": 1
    }

    """

    queryset = Order.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by(
            "-time_sell"
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderSerializer
        return OrderCreateUpdateSerializer

    # limitation for only one order open, to prevent from having two opened_order
    def perform_update(self, serializer):
        change_sts_to_started = serializer.validated_data.get("status", 0)
        open_order = self.get_object()
        if change_sts_to_started == Order.Status.STARTED and open_order:
            raise ValidationError(
                "You have active order opened, Please postpone or delete it"
            )
        if open_order.worker_owner != self.request.user:
            raise ValidationError("Only owner can update the order")

        serializer.save()

    def perform_destroy(self, instance):
        # Validation only owner of order can delete the order
        if instance.worker_owner == self.request.user:
            instance.delete()
        else:
            raise ValidationError("Only owner can delete the order")


class OrderItemListCreateAPIView(ListCreateAPIView):
    """
    endpoint: adding order-item(ice)

    """

    serializer_class = OrderItemCreateSerializer
    queryset = OrderItem.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # limitation for open order first ,then add order-item(ice)
        active_order = Order.objects.filter(
            worker_owner=request.user, status=Order.Status.STARTED
        ).first()
        if not active_order:
            raise ValidationError(
                "No opened order ,please create one to add order_items(ices)"
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        active_order = Order.objects.filter(
            worker_owner=self.request.user, status=Order.Status.STARTED
        ).first()
        serializer.save(order=active_order.id)


class DeleteOrderItem(RetrieveDestroyAPIView):
    """
    endpoint: deleting order-item(ice) from the current cart
    """

    queryset = OrderItem.objects.filter(order__status=Order.Status.STARTED)
    serializer_class = OrderItemCreateSerializer

    def get_queryset(self):
        queryset = OrderItem.objects.filter(
            order__status=Order.Status.STARTED, order__worker_owner=self.request.user
        )
        return queryset

    # user can delete only order-items(ices) from current open order
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (TypeError, ValueError, ValidationError):
            raise ValidationError(
                "For this user there is no open current order and no orderitem"
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email"]


class UserProfileUpdate(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
