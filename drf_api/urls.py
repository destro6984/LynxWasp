from django.urls import include, path

from .views import (
    AddFlavourCreateAPIView,
    AddIceCreateAPIView,
    DeleteOrderItem,
    OrderChangeView,
    OrderCrateView,
    OrderItemCreate,
    OrdersListAPIView,
    UserListView,
    UserProfileUpdate,
)

urlpatterns = [
    path("ices/", AddIceCreateAPIView.as_view(), name="create-ice"),
    path("flavours/", AddFlavourCreateAPIView.as_view(), name="add-flavour"),
    path("orders/", OrdersListAPIView.as_view(), name="order-list"),
    path("order-manage/<int:id>", OrderChangeView.as_view(), name="order-manage"),
    path("orders/", OrderCrateView.as_view(), name="order-create"),
    path("order-items/", OrderItemCreate.as_view(), name="orderitem-create"),
    path("order-item/<int:pk>", DeleteOrderItem.as_view(), name="orderitem-delete"),
    # DRF API auth-users
    path("users/", UserListView.as_view(), name="users-list"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("user-profile", UserProfileUpdate.as_view(), name="user-profile"),
]
