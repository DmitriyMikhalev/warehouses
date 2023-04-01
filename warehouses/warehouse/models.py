from datetime import datetime as dt
from datetime import timedelta, timezone

from django.core.validators import (EmailValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db.models import (CASCADE, CharField, DateTimeField, F, ForeignKey,
                              Model, PositiveIntegerField,
                              PositiveSmallIntegerField, Q)
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from warehouses.settings import (MAX_ADDRESS_LENGTH, MAX_EMAIL_LENGTH,
                                 MAX_NAME_LENGTH, MAX_PRODUCT_NAME_LENGTH,
                                 MAX_WAREHOUSE_NAME_LENGTH, MIN_ARTICLE_NUMBER,
                                 NAX_VEHICLE_BRAND_LENGTH,
                                 ORDER_DAYS_MAX_OFFSET, ORDER_DAYS_MIN_OFFSET,
                                 TIMEZONE_OFFSET)


class Owner(Model):
    email = CharField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        validators=(
            EmailValidator(
                message='Некорректный формат электронного адреса.'
            ),
        )
    )
    first_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Имя'
    )
    last_name = CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Фамилия'
    )

    class Meta:
        db_table = 'owner'
        managed = False
        ordering = ('-id',)
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(Model):
    article_number = PositiveIntegerField(
        unique=True,
        validators=(
            MinValueValidator(
                limit_value=MIN_ARTICLE_NUMBER,
                message=f'Артикул должен быть не меньше {MIN_ARTICLE_NUMBER}.'
            ),
        ),
        verbose_name='Артикул'
    )
    name = CharField(
        db_index=True,
        max_length=MAX_PRODUCT_NAME_LENGTH,
        verbose_name='Название'
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('name', 'article_number'),
                name='product_article_index'
            ),
        )
        db_table = 'product'
        managed = False
        ordering = ('-id',)
        index_together = ('name', 'article_number'),
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'Арт. #{self.article_number} ({self.name})'


class ProductShopOrder(Model):
    date_end = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MIN_OFFSET)
            ),
            MaxValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MAX_OFFSET)
            ),
        ),
        verbose_name='Конец'
    )
    date_start = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MIN_OFFSET)
            ),
            MaxValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MAX_OFFSET)
            ),
        ),
        verbose_name='Начало'
    )
    payload = PositiveSmallIntegerField(
        verbose_name='Масса товара (т)'
    )
    product = ForeignKey(
        on_delete=CASCADE,
        related_name='orders',
        to='Product',
        verbose_name='Товар'
    )
    shop = ForeignKey(
        on_delete=CASCADE,
        related_name='orders',
        to='Shop',
        verbose_name='Магазин'
    )
    vehicle = ForeignKey(
        on_delete=CASCADE,
        related_name='orders',
        to='Vehicle',
        verbose_name='Машина'
    )
    warehouse = ForeignKey(
        on_delete=CASCADE,
        related_name='orders',
        to='Warehouse',
        verbose_name='Склад'
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(date_end__gt=F('date_start')),
                name='Дата начала раньше даты конца'
            ),
        )
        db_table = 'product_shop_order'
        managed = False
        ordering = ('date_start',)
        verbose_name = 'Заказ магазина'
        verbose_name_plural = 'Заказы магазина'

    def __str__(self):
        return f'{self.shop[5:]}: заказ на {self.date_start.date()}'


class ProductTransit(Model):
    payload = PositiveSmallIntegerField(
        verbose_name='Масса поставки (т)'
    )
    product = ForeignKey(
        on_delete=CASCADE,
        related_name='product_transit',
        to='Product',
        verbose_name='Товар'
    )
    transit = ForeignKey(
        on_delete=CASCADE,
        related_name='product_transit',
        to='Transit',
        verbose_name='Поставка'
    )

    class Meta:
        db_table = 'product_transit'
        managed = False
        ordering = ('id',)
        verbose_name = 'Товар в поставке'
        verbose_name_plural = 'Товары в поставке'

    def __str__(self):
        return f'Состав поставки {self.transit.date_start.date()}'


class ProductWarehouse(Model):
    payload = PositiveIntegerField(
        verbose_name='Масса товара (т)'
    )
    product = ForeignKey(
        on_delete=CASCADE,
        related_name='product_warehouse',
        to='Product',
        verbose_name='Товар'
    )
    warehouse = ForeignKey(
        on_delete=CASCADE,
        related_name='product_warehouse',
        to='Warehouse',
        verbose_name='Склад'
    )

    class Meta:
        db_table = 'product_warehouse'
        managed = False
        ordering = ('id',)
        verbose_name = 'Товар на складе'
        verbose_name_plural = 'Товары на складе'

    def __str__(self):
        return f'Товар {self.product} на складе {self.warehouse}'


class Shop(Model):
    address = CharField(max_length=MAX_ADDRESS_LENGTH, verbose_name='Адрес')
    owner = ForeignKey(
        on_delete=CASCADE,
        related_name='shops',
        to='Owner',
        verbose_name='Владелец'
    )

    class Meta:
        db_table = 'shop'
        managed = False
        ordering = ('id',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return f'Магазин по адресу {self.address}'


class Transit(Model):
    date_end = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MIN_OFFSET)
            ),
            MaxValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MAX_OFFSET)
            ),
        ),
        verbose_name='Конец'
    )
    date_start = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MIN_OFFSET)
            ),
            MaxValueValidator(
                limit_value=dt.now(
                    tz=timezone(timedelta(hours=TIMEZONE_OFFSET))
                ) + timedelta(days=ORDER_DAYS_MAX_OFFSET)
            ),
        ),
        verbose_name='Начало'
    )
    warehouse = ForeignKey(
        on_delete=CASCADE,
        related_name='transits',
        to='Warehouse',
        verbose_name='Склад'
    )

    class Meta:
        constraints = (
            CheckConstraint(
                check=Q(date_end__gt=F('date_start')),
                name='Дата конца позже даты начала'
            ),
        )
        db_table = 'transit'
        managed = False
        ordering = ('id',)
        verbose_name = 'Поставка на склад'
        verbose_name_plural = 'Поставки на склад'

    def __str__(self):
        return f'Поставка на {self.warehouse}: {self.date_start.date()}'


class Vehicle(Model):
    brand = CharField(
        max_length=NAX_VEHICLE_BRAND_LENGTH,
        verbose_name='Марка машины'
    )
    max_capacity = PositiveSmallIntegerField(
        verbose_name='Вместимость машины (т)'
    )
    owner = ForeignKey(
        on_delete=CASCADE,
        related_name='vehicles',
        to='Owner',
        verbose_name='Владелец'
    )

    class Meta:
        db_table = 'vehicle'
        managed = False
        ordering = ('id',)
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'{self.brand}: владелец {self.owner}'


class VehicleTransit(Model):
    transit = ForeignKey(
        on_delete=CASCADE,
        related_name='vehicle_transit',
        to='Transit',
        verbose_name='Транзит'
    )
    vehicle = ForeignKey(
        on_delete=CASCADE,
        related_name='vehicle_transit',
        to='Vehicle',
        verbose_name='Машина'
    )

    class Meta:
        db_table = 'vehicle_transit'
        managed = False
        ordering = ('id',)
        verbose_name = 'Поставка машиной'
        verbose_name_plural = 'Поставки машиной'

    def __str__(self):
        return f'{self.transit} машиной {self.vehicle}'


class Warehouse(Model):
    address = CharField(
        max_length=MAX_ADDRESS_LENGTH,
        verbose_name='Адрес склада'
    )
    max_capacity = PositiveIntegerField(
        verbose_name='Вместимость склада'
    )
    name = CharField(
        unique=True,
        max_length=MAX_WAREHOUSE_NAME_LENGTH,
        verbose_name='Название склада'
    )
    owner = ForeignKey(
        on_delete=CASCADE,
        related_name='warehouses',
        to='Owner',
        verbose_name='Владелец склада'
    )

    class Meta:
        managed = False
        db_table = 'warehouse'

    def __str__(self):
        return f'"{self.name}" по адресу {self.address}'
