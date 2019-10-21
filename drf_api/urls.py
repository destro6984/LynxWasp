from django.conf.urls import url
from django.db import router
from django.urls import include
from rest_framework import routers

from .views import AddIceCreateAPIView, AddFlavourCreateAPIView
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 99a397cf8c0d34db95c537a6cf444b4c7d5fa1ad

urlpatterns = [
    # url(r'^$', OrdersListAPIView.as_view(), name='order-list'),
    url(r'create-ice/$', AddIceCreateAPIView.as_view(), name='create-ice'),
    url(r'add-flavour/$', AddFlavourCreateAPIView.as_view(), name='add-flavour'),

]
<<<<<<< HEAD
=======

urlpatterns = [
    # url(r'^$', OrdersListAPIView.as_view(), name='order-list'),
    url(r'create-ice/$', AddIceCreateAPIView.as_view(), name='create-ice'),
    url(r'add-flavour/$', AddFlavourCreateAPIView.as_view(), name='add-flavour'),

]
>>>>>>> usahe drf check add falvour
=======
>>>>>>> 99a397cf8c0d34db95c537a6cf444b4c7d5fa1ad
