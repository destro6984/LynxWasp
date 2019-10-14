from django.conf.urls import url

from .views import OrdersListAPIView, AddIceCreateAPIView

urlpatterns=[
    url(r'^$', OrdersListAPIView.as_view(), name='order-list'),
    url(r'create-ice/$', AddIceCreateAPIView.as_view(), name='create-ice')
]