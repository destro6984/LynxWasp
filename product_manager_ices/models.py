from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Ices(models.Model):
    price=models.DecimalField(max_digits=5,decimal_places=2)
    worker=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sell_time=models.DateField(auto_now_add=True)


class Type(models.Model):
    type=models.CharField(max_length=45)
    ice=models.ForeignKey(Ices,on_delete=models.CASCADE)
