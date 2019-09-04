from django.contrib import admin
from django.urls import path, include

from product_manager_ices.views import Homepage, AddIce, IcesView, CreateOrder, delete_orderitem, \
    change_status_order_for_finish

urlpatterns = [


    path('', Homepage.as_view(), name='homepage' ),
    path('add-ice', AddIce.as_view(), name='add-ice' ),
    path('list-ices', IcesView.as_view(), name='list-ices'),
    path('create-order', CreateOrder.as_view(), name='create-order'),
    path('delete/<id>', delete_orderitem, name='delete_oi'),
    path('finish-order/<id>',change_status_order_for_finish , name='change_to_finish'),

]
