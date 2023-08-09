from django.urls import path

from product_manager_ices.views import (
    CreateOrderItemView,
    HomepageView,
    IceView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    change_status_order_for_finish,
    delete_orderitem,
    open_order,
    postpone_order,
    reactivate_order,
)

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("ices/", IceView.as_view(), name="add-ice"),
    path("orders/delete/<int:pk>", OrderDeleteView.as_view(), name="delete-order"),
    path("orders/reactivate/<int:pk>", reactivate_order, name="reactivate-order"),
    path("orders/", OrderListView.as_view(), name="list-order"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="detail-order"),
    path("orders/open", open_order, name="open-order"),
    path("orders/postpone/<int:pk>", postpone_order, name="postpone-order"),
    path("orders/finish/<int:pk>", change_status_order_for_finish, name="finish-order"),
    path("order-items/", CreateOrderItemView.as_view(), name="create-order-item"),
    path("order-item/delete/<int:pk>", delete_orderitem, name="delete-order-item"),
]
