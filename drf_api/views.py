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
    # working adding order testing
    def get(self,request):
        order = [order for order in Order.objects.all()]
        serialized= OrderCreateSerializer(order, many=True)
        return Response(serialized.data)
    def post(self,request):
        serialized = OrderCreateSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save(status=1,worker_owner=self.request.user)
            return Response(serialized.data)
        return Response(serialized.errors,status=400)



# class OrderItemCreate(ListCreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemCreateSerializer
class OrderItemCreate(APIView):
    def get(self,request):
        orderitem = [order for order in OrderItem.objects.all()]
        serialized= OrderItemCreateSerializer(orderitem, many=True)
        return Response(serialized.data)
    def post(self,request):
        serialized=OrderItemCreateSerializer(data=request.data)
        activeorder=Order.objects.filter(worker_owner=request.user, status=1).first()
        if serialized.is_valid():
            serialized.save(order=[activeorder.id])
            return Response(serialized.data,status=201)
        return Response(serialized.errors, status=400)



    #
    # def put(self,request):
    #     serializer_orderitem =OrderItemCreateSerializer(data=request.data)
    #     print(serializer_orderitem)
    #     if serializer_orderitem.is_valid():
    #         serializer_orderitem.save()
    #         return Response(serializer_orderitem.data)
    #     return Response(serializer_orderitem.errors, status=400)


# working adding orderitem
#     def get(self,request):
#         order = [order for order in OrderItem.objects.all()]
#         serialized= OrderItemCreateSerializer(order, many=True)
#         return Response(serialized.data)

#     def post(self,request):
#         print(request.data)
#         serialized = OrderItemCreateSerializer(data=request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data)
#         return Response(serialized.errors,status=400)

