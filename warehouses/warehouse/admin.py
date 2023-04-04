from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.admin.actions import delete_selected

from .forms import (OrderForm, ProductTransitInlineForm,
                    ProductWarehouseInlineForm, VehicleTransitInlineForm)
from .models import (Order, Owner, Product, ProductTransit, ProductWarehouse,
                     Shop, Transit, Vehicle, VehicleTransit, Warehouse)

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
        """
        If warehouse exists, shows immutable products in amount current
        warehouse has products, else max count of products None that means
        unlimited.
        """
        return obj.product_warehouse.count() if obj is not None else None


class VehicleTransitInline(DefaultInline):
    # прикрутить проверку, что машина свободна (машины)
    model = VehicleTransit
    min_num = 1
    can_delete = True
    form = VehicleTransitInlineForm

    def get_max_num(self, request, obj=None):
        return Vehicle.objects.count()


class VehicleInline(DefaultInline):
    model = Vehicle
    can_delete = True


class WarehouseInline(DefaultInline):
    model = Warehouse
    readonly_fields = ('id', 'max_capacity')


class OrderInline(DefaultInline):
    verbose_name_plural = 'Осуществленные заказы магазина'
    model = Order
    fields = (
        'date_start',
        'date_end',
        'warehouse',
        'vehicle'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(accepted=True)

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
        'warehouse',
        'vehicle'
    )
    search_fields = ('date_start', 'date_end',)
    list_filter = ('warehouse', 'vehicle', 'accepted')
    date_hierarchy = 'date_start'
    list_display_links = None
    actions = ('accept_order',)
    form = OrderForm

    @admin.action(description='Осуществлено')
    def accept_order(self, request, queryset):
        for order in queryset.filter(accepted=False):
            order.accepted = True
            order.save()


class ShopInline(ReadOnlyInlineMixin, DefaultInline):
    model = Shop
    show_change_link = True


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
    inlines = (ProductWarehouseInline,)

    def get_readonly_fields(self, request, obj=None):
        return ('max_capacity',) if obj is not None else ()


@admin.register(Transit)
class TransitAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'date_start', 'date_end', 'warehouse')
    list_filter = ('date_start', 'date_end', 'accepted')
    search_fields = ('date_start', 'date_end')
    readonly_fields = ('accepted',)
    date_hierarchy = 'date_start'
    inlines = (ProductTransitInline, VehicleTransitInline)

    def gets_readonly_fields(self, request, obj=None):
        return ('accepted',) if obj is None else ()

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


@admin.register(Shop)
class ShopAdmin(ModelAdminListPerPage20):
    list_display = ('id', 'address', 'owner')
    list_display_links = ('address',)
    search_fields = ('owner', 'address')
    inlines = (OrderInline,)
