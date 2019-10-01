"""Twitecs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from django.contrib.auth import views as auth_views

from .views import Registration, DeleteUser
from . import views


urlpatterns = [

    url(r"^login/$", auth_views.LoginView.as_view(template_name="users_app/login.html"), name='login'),
    url(r"^logout/$", auth_views.LogoutView.as_view(template_name="users_app/logout.html"), name='logout'),
    url(r"^register/$", Registration.as_view(), name='register'),
    url(r"^profile/$", views.profile_user, name='profile'),
    url(r"^delete/(?P<pk>\d*$)", DeleteUser.as_view(), name='delete'),
    url(r"^update/(?P<pk>\d$)", views.profile_user, name='update'),



]
