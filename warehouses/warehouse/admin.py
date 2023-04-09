from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.contrib.admin.actions import delete_selected
from django.db.models import Sum

from .forms import ShopForm
from .inlines import (OrderInline, ProductOrderInline, ProductTransitInline,
                      ProductWarehouseInline, ShopInline, TransitInline,
                      VehicleInline, VehicleOrderInline, VehicleTransitInline,
                      WarehouseInline)
from .mixins import NoChangePermissionMixin
from .models import (Order, Owner, Product, ProductWarehouse, Shop, Transit,
                     Vehicle, Warehouse)
from .utils import get_diff_order, get_diff_transit

delete_selected.short_description = 'Удалить'


class ModelAdmin(BaseModelAdmin):
    list_per_page = settings.LIST_PER_PAGE


@admin.register(Order)
class OrderAdmin(NoChangePermissionMixin, ModelAdmin):
    actions = ('accept_order',)
    date_hierarchy = 'date_start'
    inlines = (ProductOrderInline, VehicleOrderInline)
    list_display = ('id', 'accepted', 'date_start', 'date_end', 'shop',
                    'warehouse')
    list_filter = ('warehouse', 'accepted', 'date_start', 'date_end')
    readonly_fields = ('accepted', 'id')
    search_fields = ('date_start', 'date_end')

    @admin.action(description='Осуществлено')
    def accept_order(self, request, queryset):
        """
        If product's payload from order is equal to value in related warehouse,
        delete object from ProductWarehouse model, else substracts difference
        value; mark the order as accepted.
        """
        for order in queryset.filter(accepted=False):
            for product, diff in get_diff_order(order).items():
                if (obj := ProductWarehouse.objects.get(
                        warehouse=order.warehouse,
                        product=product
                   )).payload == diff:
                    obj.delete()
                else:
                    obj.payload = obj.payload - diff
                    obj.save()

            order.accepted = True
            order.save()


@admin.register(Owner)
class OwnerAdmin(ModelAdmin):
    inlines = (VehicleInline, WarehouseInline, ShopInline)
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('first_name',)
    search_fields = ('email', 'first_name', 'last_name')

    def get_inlines(self, request, obj=None):
        """
        If owner is being created inlines (vehicle, warehouse and shop) will
        not be shown. In other cases all inlines will be shown.
        """
        return (VehicleInline, WarehouseInline, ShopInline) if obj else ()


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('id', 'name', 'article_number')
    list_display_links = ('name',)
    search_fields = ('article_number', 'name')


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    form = ShopForm
    list_display = ('id', 'name', 'address', 'owner', 'unaccepted_order_count')
    list_display_links = ('name',)
    list_filter = ('owner', )
    search_fields = ('address', 'owner')

    def get_inlines(self, request, obj=None):
        """
        If shop is being created inline (Order) will not be shown.
        In other cases inline will be shown.
        """
        return (OrderInline,) if obj else ()

    def unaccepted_order_count(self, obj):
        """
        Get count of orders related to current warehouse that was not accepted.
        """
        return Order.objects.filter(accepted=False, shop=obj).count()

    unaccepted_order_count.short_description = 'Ожидает поставок'


@admin.register(Transit)
class TransitAdmin(NoChangePermissionMixin, ModelAdmin):
    actions = ('accept_transit',)
    date_hierarchy = 'date_start'
    inlines = (ProductTransitInline, VehicleTransitInline)
    list_display = ('id', 'accepted', 'date_start', 'date_end', 'warehouse')
    list_filter = ('date_start', 'date_end', 'accepted')
    readonly_fields = ('accepted', 'id')
    search_fields = ('date_start', 'date_end')

    @admin.action(description='Осуществлено')
    def accept_transit(self, request, queryset):
        """
        If product from transit is not presented in related warehouse, create
        that row and set difference value as payload else add difference value
        to payload; mark the transit as accepted.
        """
        for transit in queryset.filter(accepted=False):
            for product, diff in get_diff_transit(transit).items():
                if (obj := ProductWarehouse.objects.filter(
                    warehouse=transit.warehouse,
                    product=product
                ).first()) is not None:
                    obj.payload = obj.payload + diff
                    obj.save()
                else:
                    ProductWarehouse.objects.create(
                        product=product,
                        warehouse=transit.warehouse,
                        payload=diff
                    )

            transit.accepted = True
            transit.save()


@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    list_display = ('id', 'brand', 'max_capacity', 'owner', 'vin')
    list_display_links = ('brand',)
    list_filter = ('owner', 'brand')
    search_fields = ('max_capacity', 'vin')

    def get_readonly_fields(self, request, obj=None):
        """If vehicle is being created allows to set max_capacity."""
        return ('max_capacity',) if obj is not None else ()


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = ('id', 'address', 'name', 'total_payload', 'max_capacity',
                    'owner', 'unaccepted_transit_count')
    list_display_links = ('address',)
    search_fields = ('address', 'name', 'email', 'owner')
    list_filter = ('owner',)

    def get_inlines(self, request, obj=None):
        """
        Allows show only products in warehouse while warehouse is being
        created. In other cases shows transits additionally.
        """
        return (ProductWarehouseInline, TransitInline) if obj else (
            ProductWarehouseInline,
        )

    def get_readonly_fields(self, request, obj=None):
        """If warehouse is being created allows to set max_capacity."""
        return ('max_capacity',) if obj is not None else ()

    def total_payload(self, obj):
        """
        Additional column for display that means current warehouse's payload.
        """
        return obj.product_warehouse.all().aggregate(
            sum=Sum('payload')
        ).get('sum') or 0

    def unaccepted_transit_count(self, obj):
        """
        Additional column for display that means transits count which were not
        accepted.
        """
        return Transit.objects.filter(warehouse=obj, accepted=False).count()

    total_payload.short_description = 'Текущая загрузка (т)'
    unaccepted_transit_count.short_description = 'Ожидает поставок'
