from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProfileUser, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(
            user=instance, image_from_cl="image/upload/v1565630684/non_existing_id.png"
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profileuser.save(force_insert=False)
