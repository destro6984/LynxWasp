from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import dateformat, timezone


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # CLOUDINARY DOCS :https://cloudinary.com/documentation/image_transformation_reference
    image_from_cl = CloudinaryField(
        "image",
        public_id=str(dateformat.format(timezone.now(), "Y-m-d H:i:s")),
        transformation=[
            {"width": 150, "height": 150, "radius": "max", "crop": "fit"},
        ],
    )
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return (
            f" {self.user.username} Profile, First_name: {self.user.first_name}, Last_name: {self.user.last_name},"
            f" Location: {self.location}, Birth Date: {self.birth_date}"
        )
