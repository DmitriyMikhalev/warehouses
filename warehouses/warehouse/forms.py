from django.core.exceptions import NON_FIELD_ERRORS
from django.db.models import Sum
from django.forms import ModelForm, ValidationError

from .models import (ProductOrder, ProductTransit, ProductWarehouse, Shop,
                     VehicleOrder, VehicleTransit, Warehouse, Order)
from .utils import (get_datetime_local_timezone, get_inline_sum,
                    get_product_payload_diff, has_inline_duplicates,
                    is_vehicle_available)


class ProductWarehouseInlineForm(ModelForm):
    def clean(self):
        """при создании склада проверка инлайна"""
        cleaned_data = super().clean()

        if (max_capacity := self.data.get('max_capacity')) != '':
            max_capacity = int(max_capacity)
            new_payload = get_inline_sum(
                pattern=r'^product_warehouse-[0-9]+-payload$',
                data=self.data
            )

            if new_payload > max_capacity:
                raise ValidationError(
                    message='Склад не сможет вместить такое количество товаров'
                            + f' ({new_payload} > {max_capacity}).'
                )

        return cleaned_data

    class Meta:
        fields = ('product', 'payload')
        model = ProductWarehouse


class ProductOrderInlineForm(ModelForm):
    def clean_payload(self):
        if self.data.get('warehouse') != '':
            product = self.cleaned_data.get('product')
            required_payload = self.cleaned_data.get('payload')
            warehouse_id = self.data.get('warehouse')
            warehouse = Warehouse.objects.filter(pk=warehouse_id).first()

            date_start = self.data.get('date_start_0')
            time_start = self.data.get('date_start_1')
            date_end = self.data.get('date_end_0')
            time_end = self.data.get('date_end_1')

            if all(i for i in (date_start, time_start, date_end, time_end)):
                date_start = get_datetime_local_timezone(
                    date=date_start,
                    time=time_start
                )
                date_end = get_datetime_local_timezone(
                    date=date_end,
                    time=time_end
                )
                diff = get_product_payload_diff(
                    warehouse=warehouse,
                    product=product,
                    date_start=date_start
                )
                current_payload = ProductWarehouse.objects.filter(
                    warehouse=warehouse,
                    product=product
                ).aggregate(sum=Sum('payload')).get('sum') or 0

                if required_payload > (val := current_payload + diff):
                    raise ValidationError(
                        message='На складе нет такого количества товара'
                                + f' (доступно {val} т).'
                    )

        return self.cleaned_data.get('payload')

    class Meta:
        fields = ('product', 'payload')
        model = ProductOrder


class ProductTransitInlineForm(ModelForm):
    def clean(self):
        """при создании поставки проверка инлайна"""
        cleaned_data = super().clean()

        if (warehouse_id := self.data.get('warehouse')) != '':
            warehouse = Warehouse.objects.get(pk=warehouse_id)
            new_payload = get_inline_sum(
                pattern=r'^product_transit-[0-9]+-payload$',
                data=self.data
            )
            current_payload = ProductWarehouse.objects.filter(
                warehouse=warehouse
            ).aggregate(sum=Sum('payload')).get('sum') or 0

            if (val := current_payload + new_payload) > warehouse.max_capacity:
                raise ValidationError(
                    message='Склад не сможет вместить такое количество товаров'
                            + f' ({val} > {warehouse.max_capacity}).'
                )

        return cleaned_data

    class Meta:
        fields = ('product', 'payload')
        model = ProductTransit


class VehicleInlineBaseForm(ModelForm):
    def clean_vehicle(self):
        vehicle = self.cleaned_data.get('vehicle')
        date_start = self.data.get('date_start_0')
        time_start = self.data.get('date_start_1')
        date_end = self.data.get('date_end_0')
        time_end = self.data.get('date_end_1')

        if all(i for i in (date_start, time_start, date_end, time_end)):
            date_start = get_datetime_local_timezone(
                date=date_start,
                time=time_start
            )
            date_end = get_datetime_local_timezone(
                date=date_end,
                time=time_end
            )

            if not is_vehicle_available(
                vehicle=vehicle,
                date_start=date_start,
                date_end=date_end
            ):
                raise ValidationError(message='Машина занята в это время.')

        return vehicle


class VehicleOrderInlineForm(VehicleInlineBaseForm):
    pattern = r'^vehicle_order-[0-9]+-vehicle$'

    class Meta:
        fields = ('vehicle',)
        model = VehicleOrder


class VehicleTransitInlineForm(VehicleInlineBaseForm):
    pattern = r'^vehicle_transit-[0-9]+-vehicle$'

    class Meta:
        fields = ('vehicle',)
        model = VehicleTransit


class ShopForm(ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Shop.objects.filter(name=name).exists():
            raise ValidationError(
                message='Магазин с таким названием уже существует.'
            )

        return name

    class Meta:
        fields = ('address', 'name', 'owner')
        model = Shop
