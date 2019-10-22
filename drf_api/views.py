from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers, OrderListSerializer
from product_manager_ices.models import Order


class AddIceCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AddIcesSerializers


class AddFlavourCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AddFlavourSerializers

class OrdersListAPIView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderListSerializer

    # checkout viewsets or just list and update mixin
    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset

class OrderChangeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderListSerializer
    lookup_field = "id"


    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        queryset = Order.objects.filter(worker_owner=self.request.user, status=1)
        if queryset.exists():
            raise ValidationError('You have active order opened, Please postpone or delete it')
        serializer.save()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
