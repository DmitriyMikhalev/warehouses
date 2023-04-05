from django.db.models import Sum
from django.forms import ModelForm, ValidationError

from .models import ProductTransit, ProductWarehouse, Transit, VehicleTransit
from .utils import (get_datetime_deleted_timezone, get_inline_objs_id,
                    get_inline_sum, is_vehicle_available)


class TransitForm(ModelForm):
    def clean(self):
        return super().clean()

    class Meta:
        fields = ('accepted', 'date_start', 'date_end', 'warehouse')
        model = Transit


class ProductOrderInlineForm(ModelForm):
    # прикрутить проверку на продукт
    class Meta:
        fields = ()


class ProductWarehouseInlineForm(ModelForm):
    def clean(self):
        """при создании склада проверка инлайна"""
        cleaned_data = super().clean()
        warehouse = cleaned_data['warehouse']
        new_payload = get_inline_sum(
            pattern=r'^product_warehouse-[0-9]+-payload$',
            data=self.data
        )

        if new_payload > warehouse.max_capacity:
            raise ValidationError(
                message='Склад не сможет вместить такое количество товаров ('
                        + f'{new_payload} > {warehouse.max_capacity}).'
            )

        return cleaned_data

    class Meta:
        fields = ('product', 'payload')
        model = ProductWarehouse


class ProductTransitInlineForm(ModelForm):
    def clean(self):
        """при создании поставки проверка инлайна"""
        cleaned_data = super().clean()
        product_ids = get_inline_objs_id(
            pattern=r'^product_transit-[0-9]+-product$',
            data=self.data
        )

        if len(set(product_ids)) != len(product_ids):
            raise ValidationError(
                message='Запрещены дубликаты товаров.'
            )

        warehouse = cleaned_data.get('transit').warehouse
        new_payload = get_inline_sum(
            pattern=r'^product_transit-[0-9]+-payload$',
            data=self.data
        )
        current_payload = ProductWarehouse.objects.filter(
            warehouse=warehouse
        ).aggregate(sum=Sum('payload')).get('sum') or 0

        if (val := current_payload + new_payload) > warehouse.max_capacity:
            raise ValidationError(
                message='Склад не сможет вместить такое количество товаров ('
                        + f'{val} > {warehouse.max_capacity}).'
            )

        return cleaned_data

    class Meta:
        fields = ('product', 'payload')
        model = ProductTransit


class VehicleTransitInlineForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        vehicle_ids = get_inline_objs_id(
            pattern=r'^vehicle_transit-[0-9]+-vehicle$',
            data=self.data
        )

        if len(set(vehicle_ids)) != len(vehicle_ids):
            raise ValidationError('Запрещено повторно выбирать одну машину.')

        return cleaned_data

    def clean_vehicle(self):
        vehicle = self.cleaned_data.get('vehicle')
        date_start = self.data.get('date_start_0')
        time_start = self.data.get('date_start_1')
        date_end = self.data.get('date_end_0')
        time_end = self.data.get('date_end_1')

        date_start = get_datetime_deleted_timezone(
            date=date_start,
            time=time_start
        )
        date_end = get_datetime_deleted_timezone(
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

    class Meta:
        fields = ('vehicle',)
        model = VehicleTransit
