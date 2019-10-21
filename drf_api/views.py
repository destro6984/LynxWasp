

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly



from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers, OrderListSerializer
from product_manager_ices.models import Order


class AddIceCreateAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AddIcesSerializers


class AddFlavourCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AddFlavourSerializers




class OrdersListAPIView(RetrieveUpdateAPIView):
    serializer_class = OrderListSerializer

# checkout viewsets or just list and update mixin
    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(worker_owner=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


