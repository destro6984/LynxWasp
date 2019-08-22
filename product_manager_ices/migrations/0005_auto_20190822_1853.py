# Generated by Django 2.2.3 on 2019-08-22 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_manager_ices', '0004_order_worker_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ices_ordered',
        ),
        migrations.AddField(
            model_name='order',
            name='ices_ordered',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product_manager_ices.OrderItem'),
            preserve_default=False,
        ),
    ]
