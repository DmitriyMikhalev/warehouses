from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.CharField(unique=True, max_length=30)

    class Meta:
        constraints = [
            
        ]
        managed = False
        db_table = 'owner'

    def __str__(self):
        pass


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    article_number = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'product'
        unique_together = (('name', 'article_number'),)


class ProductShopOrder(models.Model):
    product = models.ForeignKey(Product, models.CASCADE)
    shop = models.ForeignKey('Shop', models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', models.CASCADE)
    payload = models.SmallIntegerField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product_shop_order'


class ProductTransit(models.Model):
    transit = models.ForeignKey('Transit', models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    payload = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'product_transit'


class ProductWarehouse(models.Model):
    warehouse = models.ForeignKey('Warehouse', models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    payload = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'product_warehouse'


class Shop(models.Model):
    address = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'shop'


class Transit(models.Model):
    warehouse = models.ForeignKey('Warehouse', models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'transit'


class Vehicle(models.Model):
    brand = models.CharField(max_length=30)
    max_capacity = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(Owner, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'vehicle'


class VehicleTransit(models.Model):
    transit = models.ForeignKey(Transit, models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'vehicle_transit'


class Warehouse(models.Model):
    name = models.CharField(unique=True, max_length=50)
    address = models.CharField(max_length=50)
    max_capacity = models.PositiveIntegerField()
    owner = models.ForeignKey(Owner, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'warehouse'
