from django.urls import include, path
from rest_framework.schemas import get_schema_view

from .views import (
    FlavourListCreateAPIView,
    IcesListCreateAPIView,
    OrderItemListCreateAPIView,
    OrderItemRetrieveDestroyAPIView,
    OrderRetrieveUpdateDestroyAPIView,
    OrdersListCreateAPIView,
    UserListView,
    UserProfileUpdate,
)

schema_view = get_schema_view(title="Lynx&Wasp Ice Cream App")

urlpatterns = [
    path("", schema_view),
    path("ices/", IcesListCreateAPIView.as_view(), name="ices"),
    path("flavours/", FlavourListCreateAPIView.as_view(), name="flavours"),
    path("orders/", OrdersListCreateAPIView.as_view(), name="orders"),
    path(
        "orders/<int:id>",
        OrderRetrieveUpdateDestroyAPIView.as_view(),
        name="order-manage",
    ),
    path("order-items/", OrderItemListCreateAPIView.as_view(), name="order-items"),
    path(
        "order-items/<int:pk>",
        OrderItemRetrieveDestroyAPIView.as_view(),
        name="order-item-delete",
    ),
    # DRF API auth-users
    path("users/", UserListView.as_view(), name="users-list"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("user-profile", UserProfileUpdate.as_view(), name="user-profile"),
]
