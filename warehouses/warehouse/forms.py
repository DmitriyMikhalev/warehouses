from django.db.models import Sum
from datetime import datetime, timezone
from django.forms import ModelForm, ValidationError

from .models import Order, ProductTransit, ProductWarehouse, VehicleTransit, Vehicle, Transit
from .utils import get_inline_sum, get_now_datetime, is_vehicle_available, get_inline_objs_id


class OrderForm(ModelForm):
    class Meta:
        fields = (
            'date_start',
            'date_end',
            'shop',
            'vehicle',
            'warehouse'
        )
        model = Order


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
        print(cleaned_data)
        warehouse = cleaned_data['transit'].warehouse
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
        transit = cleaned_data.get('transit')
        vehicle_ids = get_inline_objs_id(
            pattern=r'^vehicle_transit-[0-9]+-vehicle$',
            data=self.data
        )

        if len(set(vehicle_ids)) != len(vehicle_ids):
            raise ValidationError('Запрещено выбирать дважды одну машину.')

        for vehicle in Vehicle.objects.filter(pk__in=vehicle_ids):
            if not is_vehicle_available(
                vehicle=vehicle,
                date_start=transit.date_start,
                date_end=transit.date_end
            ):
                raise ValidationError(f'Машина {vehicle} занята в это время.')

        return cleaned_data

    class Meta:
        fields = ('vehicle',)
        model = VehicleTransit
