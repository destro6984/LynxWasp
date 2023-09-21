from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_api.serializers import (
    AddFlavourSerializers,
    AddIcesSerializers,
    OrderCreateSerializer,
    OrderItemCreateSerializer,
    OrderListSerializer,
    UserSerializer,
)
from product_manager_ices.models import Order, OrderItem
from users_app.models import User


class AddIceCreateAPIView(CreateAPIView):
    """
    endpoint for adding types of ice
    """

    permission_classes = [IsAdminUser]
    serializer_class = AddIcesSerializers


class AddFlavourCreateAPIView(CreateAPIView):
    """
    endpoint for adding flavours
    """

    serializer_class = AddFlavourSerializers


class OrdersListAPIView(ListAPIView):
    """
    endpoint list of orders
    search
    status-choices=1-Started/2-postponed/3-finished
    """

    serializer_class = OrderListSerializer

    # Order-detail only for owner of order/ simple search of order
    def get_queryset(self):
        search = self.request.query_params.get("q", None)
        if search is not None:
            queryset = (
                Order.objects.filter(
                    Q(worker_owner__username__icontains=search)
                    | Q(time_sell__icontains=search)
                    | Q(orderitem__flavour__flavour__icontains=search)
                    | Q(orderitem__ice__type__contains=search)
                )
                .order_by("-time_sell")
                .distinct()
            )
        else:
            queryset = Order.objects.filter(worker_owner=self.request.user).order_by(
                "-time_sell"
            )
        return queryset


class OrderChangeView(RetrieveUpdateDestroyAPIView):
    """
    endpoint changing order status
    endpoint for detail of order
    """

    serializer_class = OrderListSerializer
    lookup_field = "id"

    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by(
            "-time_sell"
        )
        return queryset

    # limitation for only one order open, to prevent form having two opened_order
    def perform_update(self, serializer):
        change_sts_to_started = serializer.validated_data["status"]
        open_order = Order.objects.filter(
            worker_owner=self.request.user, status=Order.Status.STARTED
        )
        if change_sts_to_started == 1 and open_order:
            raise ValidationError(
                "You have active order opened, Please postpone or delete it"
            )
        serializer.save()

    def perform_destroy(self, instance):
        # Validation only owner of order can delete the order
        if instance.worker_owner == self.request.user:
            instance.delete()
        else:
            raise ValidationError("Only owner can delete the order")


class OrderCrateView(APIView):
    """
    endpoint: adding order
    """

    def get(self, request):
        # validation if open order
        try:
            order = Order.objects.get(
                worker_owner=request.user, status=Order.Status.STARTED
            )
        except ObjectDoesNotExist:
            raise ValidationError("No open order")

        serialized = OrderCreateSerializer(order)
        return Response(serialized.data)

    def post(self, request):
        serialized = OrderCreateSerializer(data=request.data)
        open_order = Order.objects.filter(
            worker_owner=request.user, status=Order.Status.STARTED
        )
        # limitation if there is opened order
        if open_order:
            raise ValidationError(
                "You have already open order,please close it to open new one"
            )
        if serialized.is_valid():
            serialized.save(status=Order.Status.STARTED, worker_owner=self.request.user)
            return Response(serialized.data)
        return Response(serialized.errors, status=400)


class OrderItemCreate(CreateAPIView):
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
                "No opened order ,please create one to add orderitems(ices)"
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        # setting id of order to which adding order-item-ice, todo: consider different relations: foreigkey ??
        active_order = Order.objects.filter(
            worker_owner=self.request.user, status=Order.Status.STARTED
        ).first()
        serializer.save(order=[active_order.id])


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
