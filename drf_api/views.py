from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

from drf_api.serializers import OrderListSerializer, AddIcesSerializers
from product_manager_ices.models import Order, Ices


class AddIceCreateAPIView(ListCreateAPIView):
    queryset = Ices.objects.all()
    serializer_class = AddIcesSerializers


class OrdersListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()