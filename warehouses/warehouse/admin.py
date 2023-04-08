from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.admin.actions import delete_selected
from django.db.models import Sum

from .forms import (ProductTransitInlineForm, ProductWarehouseInlineForm,
                    ShopForm, TransitForm, VehicleTransitInlineForm)
from .models import (Order, Owner, Product, ProductOrder, ProductTransit,
                     ProductWarehouse, Shop, Transit, Vehicle, VehicleTransit,
                     Warehouse)

delete_selected.short_description = 'Удалить'


class ReadOnlyInlineMixin:
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ModelAdminListPerPage20(ModelAdmin):
    list_per_page = 20


class DefaultInline(TabularInline):
    extra = 0
    readonly_fields = ('id',)
    can_delete = False


class ProductTransitInline(DefaultInline):
    model = ProductTransit
    min_num = 1
    can_delete = True
    form = ProductTransitInlineForm

    def get_max_num(self, request, obj=None):
        return Product.objects.count()


class ProductWarehouseInline(DefaultInline):
    """
    Allows to inspect products at existing warehouse and create unlimited
    count of new products that have to be set at new warehouse while creating
    it.
    """
    model = ProductWarehouse
    form = ProductWarehouseInlineForm

    def get_readonly_fields(self, request, obj=None):
        """
        If warehouse already exists where is no ability to change anything.
        If warehouse is creating, products and payloads may be changed.
        """
        return ('product', 'payload') if obj is not None else ()

    def get_max_num(self, request, obj=None):
        return Product.objects.count() if obj is None else 0


class VehicleTransitInline(DefaultInline):
    model = VehicleTransit
    min_num = 1
    can_delete = True
    form = VehicleTransitInlineForm

    def get_max_num(self, request, obj=None):
        return Vehicle.objects.count()


class VehicleInline(DefaultInline):
    model = Vehicle
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class WarehouseInline(DefaultInline):
    model = Warehouse
    readonly_fields = ('id', 'max_capacity')
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class ProductOrderInline(DefaultInline):
    model = ProductOrder
    can_delete = True
    min_num = 1

    def get_max_num(self, request, obj=None):
        return Product.objects.count()


class OrderInline(DefaultInline):
    verbose_name_plural = 'Ожидаемые поставки в магазин'
    model = Order
    fields = (
        'date_start',
        'date_end',
        'warehouse'
    )
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(accepted=False)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TransitInline(DefaultInline):
    verbose_name_plural = 'Ожидаемые поставки на склад'
    model = Transit
    fields = (
        'date_start',
        'date_end'
    )
    show_change_link = True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(accepted=False)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(ModelAdminListPerPage20):
    list_display = (
        'accepted',
        'date_start',
        'date_end',
        'warehouse'
    )
    search_fields = ('date_start', 'date_end',)
    list_filter = ('warehouse', 'accepted')
    date_hierarchy = 'date_start'
    list_display_links = ('accepted',)
    actions = ('accept_order',)
    inlines = (ProductOrderInline,)
    # добавить проверку, что удаляемое значение - осуществлено
    @admin.action(description='Осуществлено')
    def accept_order(self, request, queryset):
        # Добавить изменение содержимого склада
        for order in queryset.filter(accepted=False):
            order.accepted = True
            order.save()

    def get_readonly_fields(self, request, obj=None):
        return ('accepted',) if obj is None else ()

    def has_change_permission(self, request, obj=None):
        return False


class ShopInline(DefaultInline):
    model = Shop
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Owner)
class OwnerAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('first_name',)
    search_fields = ('first_name', 'last_name', 'email')
    inlines = (VehicleInline, WarehouseInline, ShopInline)


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdminListPerPage20):
    list_display = (
        'id',
        'address',
        'name',
        'total_payload',
        'max_capacity',
        'owner',
        'unaccepted_transits_count'
    )
    list_display_links = ('address',)
    search_fields = ('address', 'name', 'email', 'owner')

    def get_inlines(self, request, obj=None):
        if obj is not None:
            return (ProductWarehouseInline, TransitInline)

        return (ProductWarehouseInline,)

    def total_payload(self, obj):
        return obj.product_warehouse.all().aggregate(
            sum=Sum('payload')
        ).get('sum') or 0

    def get_readonly_fields(self, request, obj=None):
        return ('max_capacity',) if obj is not None else ()

    def unaccepted_transits_count(self, obj):
        return Transit.objects.filter(warehouse=obj, accepted=False).count()

    unaccepted_transits_count.short_description = 'Ожидает поставок'

    total_payload.short_description = 'Текущая загрузка (т)'


@admin.register(Transit)
class TransitAdmin(ModelAdminListPerPage20):
    list_display = ('accepted', 'date_start', 'date_end', 'warehouse')
    list_filter = ('date_start', 'date_end', 'accepted')
    search_fields = ('date_start', 'date_end')
    readonly_fields = ('accepted',)
    date_hierarchy = 'date_start'
    # form = TransitForm
    inlines = (ProductTransitInline, VehicleTransitInline)

    def has_change_permission(self, request, obj=None):
        return False


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

    def get_readonly_fields(self, request, obj=None):
        return ('max_capacity',) if obj is not None else ()


@admin.register(Shop)
class ShopAdmin(ModelAdminListPerPage20):
    list_display = (
        'id',
        'name',
        'address',
        'owner',
        'unaccepted_orders_count'
    )
    list_display_links = ('name',)
    search_fields = ('owner', 'address')
    form = ShopForm

    def unaccepted_orders_count(self, obj):
        return Order.objects.filter(shop=obj, accepted=False).count()

    def get_inlines(self, request, obj=None):
        return (OrderInline,) if obj is not None else ()

    unaccepted_orders_count.short_description = 'Ожидает поставок'
