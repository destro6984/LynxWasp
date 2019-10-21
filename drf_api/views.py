

from rest_framework.generics import  CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly



from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers




class AddIceCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AddIcesSerializers


class AddFlavourCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AddFlavourSerializers




# class OrdersListAPIView(ListAPIView):
#     serializer_class = OrderListSerializer
#     queryset = Order.objects.all()