# Generated by Django 4.1.7 on 2023-04-06 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_vehicleorder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'managed': False, 'ordering': ('id',), 'verbose_name': 'Заказ магазина', 'verbose_name_plural': 'Заказы магазина'},
        ),
    ]
