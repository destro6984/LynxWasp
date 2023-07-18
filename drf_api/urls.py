from django.urls import include, path

from .views import (
    AddFlavourCreateAPIView,
    AddIceCreateAPIView,
    DeleteOrderitem,
    OrderChangeView,
    OrderCrateView,
    OrderItemCreate,
    OrdersListAPIView,
    UserListView,
    UserProfileUpdate,
)

urlpatterns = [
    path("create-ice/", AddIceCreateAPIView.as_view(), name="create-ice"),
    path("add-flavour/", AddFlavourCreateAPIView.as_view(), name="add-flavour"),
    path("order-list/", OrdersListAPIView.as_view(), name="order-list"),
    path("order-manage/<int:id>", OrderChangeView.as_view(), name="order-manage"),
    path("order-create/", OrderCrateView.as_view(), name="order-create"),
    path("orderitem-create/", OrderItemCreate.as_view(), name="orderitem-create"),
    path(
        "orderitem-delete/<int:pk>", DeleteOrderitem.as_view(), name="orderitem-delete"
    ),
    # DRF API auth-users
    path("user-list/", UserListView.as_view(), name="users-list"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("user-profile", UserProfileUpdate.as_view(), name="user-profile"),
]
