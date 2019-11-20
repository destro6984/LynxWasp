from cloudinary.forms import CloudinaryFileField
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils import timezone

from .models import ProfileUser

Years= [x for x in range(1940,2021)]


class UserRegistryForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "first_name", "last_name"]


class UpdateProfileUser(ModelForm):
    birth_date= forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget(years=Years))
    class Meta:
        model = ProfileUser
        exclude = ('user',)
    image_from_cl = CloudinaryFileField(
        options={'width': 150, 'height': 150, 'radius': 20, 'crop': "fit", 'public_id': str(timezone.now())})

class UpdateUser(ModelForm):
    class Meta:
        model = User
        fields=["last_name","first_name","email"]

