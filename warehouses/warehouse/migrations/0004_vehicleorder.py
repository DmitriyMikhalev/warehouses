# Generated by Django 4.1.7 on 2023-04-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_order_productorder_delete_productshoporder'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Машина, везущая заказ',
                'verbose_name_plural': 'Машины, везущие заказ',
                'db_table': 'vehicle_order',
                'ordering': ('id',),
                'managed': False,
            },
        ),
    ]