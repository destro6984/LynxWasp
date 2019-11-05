from django.contrib import admin
from django.urls import path, include

from product_manager_ices.views import Homepage, AddIce, CreateOrder, delete_orderitem, \
    change_status_order_for_finish, postpone_order, OrderDelete, ListOfOrders, return_order, OrderDetail, \
    open_order

urlpatterns = [


    path('', Homepage.as_view(), name='homepage' ),
    path('add-ice', AddIce.as_view(), name='add-ice' ),
    path('create-order', CreateOrder.as_view(), name='create-order'),
    path('open-order', open_order, name='open-order'),
    path('delete/<id>', delete_orderitem, name='delete_oi'),
    path('finish-order/<id>',change_status_order_for_finish , name='change_to_finish'),
    path('postpone-order/<id>',postpone_order , name='postpone_order'),
    path('delete-order/<pk>',OrderDelete.as_view() , name='delete_order'),
    path('return-order/<id>',return_order , name='return_order'),
    path('list-orders',ListOfOrders.as_view() , name='list_order'),
    path('detail-order/<pk>',OrderDetail.as_view() , name='detail-order'),

]
