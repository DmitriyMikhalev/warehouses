from django.db.models import Sum
from django.forms import ModelForm, ValidationError

from .models import (ProductTransit, ProductWarehouse, Shop, Transit,
                     VehicleTransit, Warehouse)
from .utils import (get_datetime_local_timezone, get_inline_sum,
                    has_inline_duplicates, is_vehicle_available)


class TransitForm(ModelForm):
    def clean(self):
        print(self.data)
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
        warehouse = cleaned_data.get('warehouse')

        if has_inline_duplicates(
            pattern=r'^product_warehouse-[0-9]+-product$',
            data=self.data
        ):
            raise ValidationError(
                message='Запрещены дубликаты товаров.'
            )

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

        if has_inline_duplicates(
            pattern=r'^product_transit-[0-9]+-product$',
            data=self.data
        ):
            raise ValidationError(
                message='Запрещены дубликаты товаров.'
            )

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


class VehicleTransitInlineForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        if has_inline_duplicates(
            pattern=r'^vehicle_transit-[0-9]+-vehicle$',
            data=self.data
        ):
            raise ValidationError('Запрещено повторно выбирать одну машину.')

        return cleaned_data

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
