from django.db.models import Sum
from django.forms import ModelForm, ValidationError
from django.shortcuts import get_object_or_404

from .utils import get_inline_sum, get_now_datetime

from .models import (ProductShopOrder, ProductTransit, ProductWarehouse,
                     Warehouse)


class ProductWarehouseForm(ModelForm):
    def clean_payload(self):
        data = self.cleaned_data.get('payload')

        warehouse = get_object_or_404(
            klass=Warehouse,
            name=self.data.get('name')
        )

        current_payload = ProductWarehouse.objects.filter(
            warehouse=warehouse
        ).aggregate(sum=Sum('payload')).get('sum')

        if (new_payload := current_payload + data) > warehouse.max_capacity:
            raise ValidationError(
                message=f'У склада не хватает вместимости ({new_payload} т).'
            )

        return data

    class Meta:
        fields = ('product', 'warehouse', 'payload')
        model = ProductWarehouse


class ProductTransitForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        now = get_now_datetime()
        date_transit = cleaned_data.get('transit').date_start

        warehouse = get_object_or_404(
            klass=Warehouse,
            id=self.data.get('warehouse')
        )

        new_payload = get_inline_sum(
            data=self.data,
            pattern=r'^product_transit-[0-9]+-payload$',
        )

        if new_payload > warehouse.max_capacity:
            raise ValidationError(
                message='Поставка на склад невозможна: превышена вместимость'
                        + f' ({new_payload} > {warehouse.max_capacity})'
            )

        positive_payload = ProductTransit.objects.filter(
            transit__warehouse=warehouse,
            transit__date_start__gte=now,
            transit__date_end__lte=date_transit
        ).aggregate(sum=Sum('payload')).get('sum') or 0

        negative_payload = ProductShopOrder.objects.filter(
            date_start__gte=now,
            date_end__lte=date_transit,
            warehouse=warehouse
        ).aggregate(sum=Sum('payload')).get('sum') or 0

        if ((val := new_payload + positive_payload - negative_payload) >
           warehouse.max_capacity):
            raise ValidationError(
                message='Поставка на склад невозможна: превышена вместимость'
                        + f' ({val} > {warehouse.max_capacity})'
            )

        return cleaned_data

    class Meta:
        fields = ('payload', 'product', 'transit')
        model = ProductTransit


class WarehouseForm(ModelForm):
    def clean_max_capacity(self):
        new_capacity = self.cleaned_data.get('max_capacity')

        warehouse = get_object_or_404(
            klass=Warehouse,
            name=self.data.get('name')
        )

        current_payload = warehouse.product_warehouse.all().aggregate(
            sum=Sum('payload')
        ).get('sum')

        if new_capacity < current_payload:
            raise ValidationError(
                message='Складу не хватит вместимости для уже находящихся'
                        + f' товаров ({current_payload} т).'
            )

        return new_capacity

    class Meta:
        fields = ('address', 'max_capacity', 'name', 'owner')
        model = Warehouse
