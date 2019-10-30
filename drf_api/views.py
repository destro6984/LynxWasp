from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers, OrderListSerializer, OrderCreateSerializer, \
    OrderItemCreateSerializer
from product_manager_ices.models import Order, OrderItem


class AddIceCreateAPIView(CreateAPIView):
    """
    endpoint for adding typs of ice
    """
    permission_classes = [IsAdminUser]
    serializer_class = AddIcesSerializers


class AddFlavourCreateAPIView(CreateAPIView):
    """
    endpoint for adding flvaoures
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AddFlavourSerializers


class OrdersListAPIView(ListAPIView):
    """
    endpoint list of orders
    search
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderListSerializer

    # Order-detail only for owner of order/ simple search of order
    def get_queryset(self):
        search = self.request.query_params.get('q', None)
        if search is not None:
            queryset = Order.objects.filter(Q(worker_owner__username__icontains=search) |
                                            Q(time_sell__icontains=search) |
                                            Q(ices_ordered__flavour__flavour__icontains=search) |
                                            Q(ices_ordered__ice__type__contains=search)).order_by("-time_sell").distinct()
        else:
            queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset


# probably better do this with ModelViewSet but it yet to come
class OrderChangeView(RetrieveUpdateDestroyAPIView):
    """
    endpoint changeing order status
    endpoint for detail of order
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderListSerializer
    lookup_field = "id"

    # setting order to see only for loged user
    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset

    # limitation for only one order open
    def perform_update(self, serializer):
        queryset = Order.objects.filter(worker_owner=self.request.user, status=1)
        if queryset.count() > 1:
            raise ValidationError('You have active order opened, Please postpone or delete it')
        serializer.save()


class OrderCrateView(APIView):
    # def get(self,request):
    #     order = [order for order in Order.objects.all()]
    #     serialized= OrderCreateSerializer(order, many=True)
    #     return Response(serialized.data)

    def get(self,request):
        order = [order for order in OrderItem.objects.all()]
        serialized= OrderItemCreateSerializer(order, many=True)
        return Response(serialized.data)

    def post(self,request):
        serialized = OrderItemCreateSerializer(data=request.POST)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors,status=400)
# working adding order testing
#     def post(self,request):
#         serialized = OrderCreateSerializer(data=request.POST)
#         if serialized.is_valid():
#             serialized.save(worker_owner=self.request.user)
#             return Response(serialized.data)
#         return Response(serialized.errors,status=400)



 # {
 #        "worker_owner": 1,
 #        "time_sell": "2019-10-07T20:29:58.805866+02:00",
 #        "status": 3,
 #        "ices_ordered": [
 #            {
 #                "ice": 5,
 #                "flavour": [],
 #                "quantity": 1
 #            }
 #        ]
 #    }

#
# {
#         "worker_owner": {
#             "id": 1,
#             "password": "pbkdf2_sha256$150000$Jg6mAOxOQ7d1$Wmkw21d6itrpPtwXiZDwwsyVZc8ipZD4aQ7TSO03p+8=",
#             "last_login": "2019-10-29T22:33:53.334488+01:00",
#             "is_superuser": true,
#             "username": "admin",
#             "first_name": "",
#             "last_name": "",
#             "is_staff": true,
#             "is_active": true,
#             "date_joined": "2019-10-01T22:30:10.054916+02:00",
#             "email": "ad@s.com",
#             "groups": [],
#             "user_permissions": []
#         },
#         "time_sell": "2019-10-29T22:33:57.108770+01:00",
#         "status": 1,
#         "ices_ordered": [
#             {
#                 "ice": 5,
#                 "flavour": [
#                     41,
#                     43
#                 ],
#                 "quantity": 1
#             }
#         ]
#     }
