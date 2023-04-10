from django.contrib.admin import TabularInline

from .forms import (ProductOrderInlineForm, ProductTransitInlineForm,
                    ProductWarehouseInlineForm, VehicleOrderInlineForm,
                    VehicleTransitInlineForm)
from .mixins import (MaxProductChoiceMixin, MaxVehicleChoiceMixin,
                     NoAddPermissionMixin, NoChangePermissionMixin,
                     UnacceptedFilterMixin)
from .models import (Order, ProductOrder, ProductTransit, ProductWarehouse,
                     Shop, Transit, Vehicle, VehicleOrder, VehicleTransit,
                     Warehouse)


class ImmutableTabularInline(NoAddPermissionMixin,
                             NoChangePermissionMixin,
                             TabularInline):
    can_delete = False
    show_change_link = True


class MutableTabularInline(TabularInline):
    can_delete = True
    extra = 0
    min_num = 1


class OrderInline(UnacceptedFilterMixin, ImmutableTabularInline):
    fields = ('date_start', 'date_end', 'warehouse')
    model = Order
    verbose_name_plural = 'Ожидаемые поставки в магазин'


class ProductOrderInline(MaxProductChoiceMixin, MutableTabularInline):
    form = ProductOrderInlineForm
    model = ProductOrder


class ProductTransitInline(MaxProductChoiceMixin, MutableTabularInline):
    form = ProductTransitInlineForm
    model = ProductTransit


class ProductWarehouseInline(MaxProductChoiceMixin, MutableTabularInline):
    """
    can_delete is False for disallow delete products from existing warehouses.
    """
    can_delete = False
    form = ProductWarehouseInlineForm
    min_num = 0
    model = ProductWarehouse

    def get_readonly_fields(self, request, obj=None):
        return ('product', 'payload') if obj is not None else ()


class ShopInline(ImmutableTabularInline):
    model = Shop


class TransitInline(UnacceptedFilterMixin, ImmutableTabularInline):
    fields = ('date_start', 'date_end')
    model = Transit
    verbose_name_plural = 'Ожидаемые поставки на склад'


class VehicleInline(ImmutableTabularInline):
    model = Vehicle


class VehicleOrderInline(MaxVehicleChoiceMixin, MutableTabularInline):
    form = VehicleOrderInlineForm
    model = VehicleOrder


class VehicleTransitInline(MaxVehicleChoiceMixin, MutableTabularInline):
    form = VehicleTransitInlineForm
    model = VehicleTransit


class WarehouseInline(ImmutableTabularInline):
    model = Warehouse
    readonly_fields = ('id', 'max_capacity')
