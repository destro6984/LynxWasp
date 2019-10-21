from django.conf.urls import url

from .views import AddIceCreateAPIView, AddFlavourCreateAPIView

urlpatterns = [
    # url(r'^$', OrdersListAPIView.as_view(), name='order-list'),
    url(r'create-ice/$', AddIceCreateAPIView.as_view(), name='create-ice'),
    url(r'add-flavour/$', AddFlavourCreateAPIView.as_view(), name='add-flavour'),

]