from django.contrib import admin
from django.urls import path, include

from product_manager_ices.views import Homepage, AddIce, IcesView, CreateOrder

urlpatterns = [


    path('', Homepage.as_view(), name='homepage' ),
    path('add-ice', AddIce.as_view(), name='add-ice' ),
    path('list-ices', IcesView.as_view(), name='list-ices'),
    path('create-order', CreateOrder.as_view(), name='create-order'),

]
