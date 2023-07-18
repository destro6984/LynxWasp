from django.contrib.auth import views as auth_views
from django.urls import path

from users_app.views import ProfileUserUpdate

from .views import DeleteUser, Registration

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users_app/logout.html"),
        name="logout",
    ),
    path("register/", Registration.as_view(), name="register"),
    path("profile/", ProfileUserUpdate.as_view(), name="profile"),
    path("delete/<int:pk>", DeleteUser.as_view(), name="delete"),
    path("update/<int:pk>", ProfileUserUpdate.as_view(), name="update"),
]
