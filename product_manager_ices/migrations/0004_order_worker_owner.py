# Generated by Django 2.2.3 on 2019-08-22 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product_manager_ices', '0003_remove_order_worker_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='worker_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
