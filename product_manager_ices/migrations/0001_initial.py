# Generated by Django 2.2.3 on 2019-11-28 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flavour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flavour', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Ices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_sell', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[(1, 'Started'), (2, 'Waiting'), (3, 'Finished')], default=1, max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('flavour', models.ManyToManyField(to='product_manager_ices.Flavour')),
                ('ice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_manager_ices.Ices')),
                ('order', models.ManyToManyField(related_name='orderitem', to='product_manager_ices.Order')),
            ],
        ),
    ]
