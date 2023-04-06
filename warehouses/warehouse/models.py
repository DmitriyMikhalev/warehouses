from datetime import timedelta
from django.core.validators import (EmailValidator, MaxValueValidator,
                                    MinValueValidator, RegexValidator)
from django.db.models import (CASCADE, CharField, DateTimeField, F, ForeignKey,
                              Model, PositiveIntegerField, BooleanField,
                              PositiveSmallIntegerField, Q)
from django.db.models.constraints import CheckConstraint, UniqueConstraint
from warehouses.settings import (MAX_ADDRESS_LENGTH, MAX_EMAIL_LENGTH,
                                 MAX_NAME_LENGTH, MAX_PRODUCT_NAME_LENGTH,
                                 MAX_VEHICLE_BRAND_LENGTH,
                                 MAX_WAREHOUSE_NAME_LENGTH, MIN_ARTICLE_NUMBER,
                                 ORDER_DAYS_MAX_OFFSET, ORDER_DAYS_MIN_OFFSET,
                                 VIN_LENGTH, MAX_SHOP_NAME_LENGTH)

from .utils import get_now_datetime


class Order(Model):
    accepted = BooleanField(
        default=False,
        verbose_name='Осуществлено'
    )
    date_start = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MIN_OFFSET
                )
            ),
            MaxValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MAX_OFFSET
                )
            ),
        ),
        verbose_name='Начало'
    )
    date_end = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MIN_OFFSET
                )
            ),
            MaxValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MAX_OFFSET
                )
            ),
        ),
        verbose_name='Конец'
    )
    shop = ForeignKey(
        on_delete=CASCADE,
        related_name='orders',
        to='Shop',
        verbose_name='Магазин'
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
        db_table = 'order_table'
        managed = False
        ordering = ('id',)
        verbose_name = 'Заказ магазина'
        verbose_name_plural = 'Заказы магазина'

    def __str__(self):
        return ''

    def __repr__(self):
        return f'Заказ #{self.id}'


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
                name='name_article_unique'
            ),
        )
        db_table = 'product'
        managed = False
        ordering = ('-id',)
        index_together = ('name', 'article_number'),
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'[{self.article_number}] {self.name}'

    def __repr__(self):
        return f'[{self.article_number}] {self.name}'


class ProductOrder(Model):
    payload = PositiveSmallIntegerField(
        validators=(MinValueValidator(limit_value=1),),
        verbose_name='Масса товара (т)'
    )
    order = ForeignKey(
        on_delete=CASCADE,
        related_name='product_order',
        to='Order',
        verbose_name='Заказ'
    )
    product = ForeignKey(
        on_delete=CASCADE,
        related_name='product_order',
        to='Product',
        verbose_name='Товар'
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('order', 'product'),
                name='product_order_unique'
            ),
        )
        db_table = 'product_order'
        managed = False
        ordering = ('id',)
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return ''

    def __repr__(self):
        return f'Состав заказа {self.order.date_start.date()}'


class ProductTransit(Model):
    payload = PositiveSmallIntegerField(
        validators=(MinValueValidator(limit_value=1),),
        verbose_name='Масса товара (т)'
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
        constraints = (
            UniqueConstraint(
                fields=('product', 'transit'),
                name='product_transit_unique'
            ),
        )
        db_table = 'product_transit'
        managed = False
        ordering = ('id',)
        verbose_name = 'Товар в поставке'
        verbose_name_plural = 'Товары в поставке'

    def __str__(self):
        return ''

    def __repr__(self):
        return f'Состав поставки {self.transit.date_start.date()}'


class ProductWarehouse(Model):
    payload = PositiveIntegerField(
        validators=(MinValueValidator(limit_value=1),),
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
        constraints = (
            UniqueConstraint(
                fields=('product', 'warehouse'),
                name='product_warehouse_unique'
            ),
        )
        db_table = 'product_warehouse'
        managed = False
        ordering = ('id',)
        verbose_name = 'Товар на складе'
        verbose_name_plural = 'Товары на складе'

    def __str__(self):
        return ''

    def __repr__(self):
        return f'{self.product} на {self.warehouse}'


class Shop(Model):
    address = CharField(max_length=MAX_ADDRESS_LENGTH, verbose_name='Адрес')
    name = CharField(
        db_index=True,
        max_length=MAX_SHOP_NAME_LENGTH,
        verbose_name='Название'
    )
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
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name} {self.address}'


class Transit(Model):
    accepted = BooleanField(
        default=False,
        verbose_name='Осуществлено'
    )
    date_start = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MIN_OFFSET
                )
            ),
            MaxValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MAX_OFFSET
                )
            ),
        ),
        verbose_name='Начало'
    )
    date_end = DateTimeField(
        validators=(
            MinValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MIN_OFFSET
                )
            ),
            MaxValueValidator(
                limit_value=get_now_datetime() + timedelta(
                    days=ORDER_DAYS_MAX_OFFSET
                )
            ),
        ),
        verbose_name='Конец'
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
        return ''

    def __repr__(self):
        return f'Поставка #{self.id}'


class Vehicle(Model):
    brand = CharField(
        max_length=MAX_VEHICLE_BRAND_LENGTH,
        verbose_name='Марка машины'
    )
    max_capacity = PositiveSmallIntegerField(
        validators=(MinValueValidator(limit_value=1),),
        verbose_name='Вместимость машины (т)'
    )
    owner = ForeignKey(
        on_delete=CASCADE,
        related_name='vehicles',
        to='Owner',
        verbose_name='Владелец'
    )
    vin = CharField(
        max_length=VIN_LENGTH,
        unique=True,
        validators=(
            RegexValidator(regex=r'^[0-9]{17}$'),
        ),
        verbose_name='VIN-номер'
    )

    class Meta:
        db_table = 'vehicle'
        managed = False
        ordering = ('id',)
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'

    def __str__(self):
        return f'#{self.id} {self.brand}'

    def __repr__(self):
        return f'#{self.id} {self.brand}'


class VehicleOrder(Model):
    order = ForeignKey(
        on_delete=CASCADE,
        related_name='vehicle_order',
        to='Transit',
        verbose_name='Заказ'
    )
    vehicle = ForeignKey(
        on_delete=CASCADE,
        related_name='vehicle_order',
        to='Vehicle',
        verbose_name='Машина'
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('order', 'vehicle'),
                name='order_vehicle_unique'
            ),
        )
        db_table = 'vehicle_order'
        managed = False
        ordering = ('id',)
        verbose_name = 'Машина в заказке'
        verbose_name_plural = 'Машины в заказе'

    def __str__(self):
        return ''

    def __repr__(self):
        return f'Машина {self.vehicle} в заказе {self.order.id}'


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
        constraints = (
            UniqueConstraint(
                fields=('transit', 'vehicle'),
                name='transit_vehicle_unique'
            ),
        )
        db_table = 'vehicle_transit'
        managed = False
        ordering = ('id',)
        verbose_name = 'Машина в поставке'
        verbose_name_plural = 'Машины в поставке'

    def __str__(self):
        return ''

    def __repr__(self):
        return f'Машина {self.vehicle} в поставке {self.transit.id}'


class Warehouse(Model):
    address = CharField(
        max_length=MAX_ADDRESS_LENGTH,
        verbose_name='Адрес склада'
    )
    max_capacity = PositiveIntegerField(
        validators=(MinValueValidator(limit_value=1),),
        verbose_name='Вместимость склада (т)'
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
        db_table = 'warehouse'
        managed = False
        ordering = ('id',)
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return f'[{self.name}] {self.address}'

    def __repr__(self):
        return f'[{self.name}] {self.address}'
