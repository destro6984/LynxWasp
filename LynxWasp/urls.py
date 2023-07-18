from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("product_manager_ices.urls")),
    path("api/", include("drf_api.urls")),
    path("user/", include("users_app.urls")),
]
