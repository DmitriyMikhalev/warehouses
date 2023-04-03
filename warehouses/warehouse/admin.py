from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import (Owner, Product, ProductShopOrder, ProductTransit,
                     ProductWarehouse, Shop, Transit, Vehicle, VehicleTransit,
                     Warehouse)
from .forms import ProductShopOrderForm


class ReadOnlyInlineMixin:
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DefaultInline(TabularInline):
    extra = 0
    readonly_fields = ('id',)
    can_delete = False


class ProductTransitInline(DefaultInline):
    model = ProductTransit
    # прикрутить проверку, что товар не переполнит склад


class ProductWarehouseInline(ReadOnlyInlineMixin, DefaultInline):
    model = ProductWarehouse

    def has_add_permission(self, request, obj=None):
        return False


class VehicleTransitInline(DefaultInline):
    model = VehicleTransit
    extra = 0
    readonly_fields = ('id',)

    def has_add_permission(self, request, obj=None):
        return False


class AddVehicleTransitInline(DefaultInline):
    model = VehicleTransit
    extra = 0
    fields = ('id', 'vehicle')
    # прикрутить проверку, что машина не занята
    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False

class VehicleInline(DefaultInline):
    model = Vehicle

    def has_change_permission(self, request, obj=None):
        return False


class WarehouseInline(DefaultInline):
    model = Warehouse
    readonly_fields = ('id', 'max_capacity')


class ProductShopOrderInline(DefaultInline):
    model = ProductShopOrder
    form = ProductShopOrderForm

    def has_change_permission(self, request, obj=None):
        return False


class ShopInline(ReadOnlyInlineMixin, DefaultInline):
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
    readonly_fields = ('max_capacity',)
    search_fields = ('address', 'name', 'email', 'owner')
    inlines = (ProductWarehouseInline,)


@admin.register(Transit)
class TransitAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'date_start', 'date_end', 'warehouse')
    list_filter = ('date_start', 'date_end')
    search_fields = ('date_start', 'date_end')
    # readonly_fields = ('date_start', 'date_end', 'warehouse')
    date_hierarchy = 'date_start'
    inlines = (
        ProductTransitInline,
        VehicleTransitInline,
        AddVehicleTransitInline
    )


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
