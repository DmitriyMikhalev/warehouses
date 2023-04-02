from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import (Owner, Product, ProductShopOrder, ProductTransit,
                     ProductWarehouse, Shop, Transit, Vehicle, VehicleTransit,
                     Warehouse)
from .forms import ProductWarehouseForm, WarehouseForm, ProductTransitForm


class DefaultInline(TabularInline):
    extra = 0
    readonly_fields = ('id',)
    can_delete = False


class ProductTransitInline(DefaultInline):
    model = ProductTransit
    form = ProductTransitForm
    readonly_fields = ('id', 'product', 'payload')


class ProductWarehouseInline(DefaultInline):
    model = ProductWarehouse
    form = ProductWarehouseForm
    readonly_fields = ('product', 'payload',)


class VehicleTransitInline(DefaultInline):
    model = VehicleTransit


class VehicleInline(DefaultInline):
    model = Vehicle


class WarehouseInline(DefaultInline):
    model = Warehouse
    readonly_fields = ('id', 'max_capacity')


class TransitInline(DefaultInline):
    model = Transit
    readonly_fields = (
        'date_start',
        'date_end'
    )


class ProductShopOrderInline(DefaultInline):
    model = ProductShopOrder
    readonly_fields = (
        'date_start',
        'date_end',
        'payload',
        'vehicle',
        'product',
        'warehouse'
    )


class ShopInline(DefaultInline):
    model = Shop
    show_change_link = True


class ModelAdminListPerPage20(ModelAdmin):
    list_per_page = 20


@admin.register(Owner)
class OwnerAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('first_name',)
    search_fields = ('first_name', 'last_name', 'email')
    inlines = (VehicleInline, WarehouseInline, ShopInline)


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'address', 'name', 'max_capacity', 'owner')
    list_display_links = ('address',)
    search_fields = ('address', 'name', 'email', 'owner')
    inlines = (ProductWarehouseInline, TransitInline)
    form = WarehouseForm


@admin.register(Transit)
class TransitAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'date_start', 'date_end', 'warehouse')
    list_filter = ('date_start', 'date_end')
    search_fields = ('date_start', 'date_end')
    readonly_fields = ('date_start', 'date_end', 'warehouse')
    date_hierarchy = 'date_start'
    inlines = (ProductTransitInline, VehicleTransitInline)


@admin.register(Product)
class ProductAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'name', 'article_number')
    list_display_links = ('name',)
    search_fields = ('name', 'article_number')


@admin.register(Vehicle)
class VehicleAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'brand', 'max_capacity', 'owner', 'vin')
    list_display_links = ('brand',)
    search_fields = ('brand', 'max_capacity', 'article_number', 'vin', 'owner')


@admin.register(Shop)
class ShopAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'address', 'owner')
    list_display_links = ('address',)
    search_fields = ('owner', 'address')
    inlines = (ProductShopOrderInline,)
