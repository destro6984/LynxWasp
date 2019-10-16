import itertools

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
<<<<<<< HEAD

from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers
from product_manager_ices.models import Order, Ices
=======
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers
from product_manager_ices.models import Order, Ices, Flavour
>>>>>>> usahe drf check add falvour


class AddIceCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AddIcesSerializers


class AddFlavourCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AddFlavourSerializers




# class OrdersListAPIView(ListAPIView):
#     serializer_class = OrderListSerializer
#     queryset = Order.objects.all()