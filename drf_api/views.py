from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404, ListCreateAPIView, DestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_api.serializers import AddIcesSerializers, AddFlavourSerializers, OrderListSerializer, OrderCreateSerializer, \
    OrderItemCreateSerializer
from product_manager_ices.models import Order, OrderItem



# Authors comment:
# probably it is better to use modelviewsetes, but lets keep some kind of learning path and assume it is yet to come


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

    serializer_class = AddFlavourSerializers

class OrdersListAPIView(ListAPIView):
    """
    endpoint list of orders
    search
    """
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
    endpoint changing order status
    endpoint for detail of order
    """
    serializer_class = OrderListSerializer
    lookup_field = "id"

    # setting order to see only for loged user
    def get_queryset(self):
        queryset = Order.objects.filter(worker_owner=self.request.user).order_by("-time_sell")
        return queryset

    # limitation for only one order open, to prevent from changing the order
    def perform_update(self, serializer):
        queryset = Order.objects.filter(worker_owner=self.request.user, status=1)
        if queryset.count() > 1:
            raise ValidationError('You have active order opened, Please postpone or delete it')
        serializer.save()


class OrderCrateView(APIView):
    """
    endpoint: adding order

    """
    def get(self,request):
        order = [order for order in Order.objects.all()]
        serialized= OrderCreateSerializer(order, many=True)
        return Response(serialized.data)
    def post(self,request):
        serialized = OrderCreateSerializer(data=request.data)
        open_order=Order.objects.filter(worker_owner=request.user,status=1)
        # limitation if there is opened order
        if open_order:
            raise ValidationError('You have already open order,please close it to open anotherone')
        if serialized.is_valid():
            serialized.save(status=1,worker_owner=self.request.user)
            return Response(serialized.data)
        return Response(serialized.errors,status=400)




class OrderItemCreate(APIView):
    """
    endpoint: adding orderitem(ice)

    """
    def get(self,request):
        orderitem = [order for order in OrderItem.objects.all()]
        serialized= OrderItemCreateSerializer(orderitem, many=True)
        return Response(serialized.data)
    def post(self,request):
        serialized=OrderItemCreateSerializer(data=request.data)
        # limitation for Thai ice to only 3 flavoures(poor option considering the id TODO )
        if (len(serialized.initial_data["flavour"]) > 3) and ((serialized.initial_data['ice'])== 1) :
            raise ValidationError('Thai ice can be made only from 3 flavoures')
        activeorder = Order.objects.filter(worker_owner=request.user, status=1).first()
        # limitation for open order first ,then add orderitem(ice)
        if not activeorder:
            raise ValidationError('No opened order ,please create one to add orderitems(ices)')
        if serialized.is_valid():
            # setting id of order to which adding orderitem-ice, todo: consider different realtions m2m ??
            serialized.save(orderitems=[activeorder.id])
            return Response(serialized.data,status=201)
        return Response(serialized.errors, status=400)



class DeleteOrderitem(DestroyAPIView):
    """
    endpoint: deleting form the cart
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer