from django.conf.urls import url

from .views import AddIceCreateAPIView, AddFlavourCreateAPIView, OrdersListAPIView, OrderChangeView, OrderCrateView, \
    OrderItemCreate, DeleteOrderitem

urlpatterns = [

    url(r'create-ice/$', AddIceCreateAPIView.as_view(), name='create-ice'),
    url(r'add-flavour/$', AddFlavourCreateAPIView.as_view(), name='add-flavour'),
    url(r'order-list/$', OrdersListAPIView.as_view(), name='order-list'),
    url(r'order-manage/(?P<id>(\d)+)$', OrderChangeView.as_view(), name='order-manage'),
    url(r'order-create/$', OrderCrateView.as_view(), name='order-create'),
    url(r'orderitem-create/$', OrderItemCreate.as_view(), name='orderitem-create'),
    url(r'orderitem-delete/(?P<pk>(\d)+)', DeleteOrderitem.as_view(), name='orderitem-delete'),


]
