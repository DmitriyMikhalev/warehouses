from django.db.models import Sum
from django.forms import ModelForm, ValidationError

from .models import ProductShopOrder, ProductTransit, ProductWarehouse
from .utils import get_now_datetime, is_vehicle_available


class ProductShopOrderForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        required_payload = cleaned_data.get('payload')
        date_start = cleaned_data.get('date_start')
        date_end = cleaned_data.get('date_end')
        product = cleaned_data.get('product')
        vehicle = cleaned_data.get('vehicle')
        warehouse = cleaned_data.get('warehouse')

        current_payload = ProductWarehouse.objects.filter(
            product=product,
            warehouse=warehouse
        ).aggregate(sum=Sum('payload')).get('sum') or 0

        positive_payload_before_start = ProductTransit.objects.filter(
            product=product,
            transit__warehouse=warehouse,
            transit__date_start__gte=get_now_datetime(),
            transit__date_end__lt=date_start
        ).aggregate(sum=Sum('payload')).get('sum') or 0

        negative_payload_before_start = ProductShopOrder.objects.filter(
            product=product,
            warehouse=warehouse,
            date_start__gte=get_now_datetime(),
            date_end__lt=date_start
        ).aggregate(sum=Sum('payload')).get('sum') or 0

        delta = positive_payload_before_start - negative_payload_before_start

        if (val := current_payload + delta) < required_payload:
            raise ValidationError(
                message='Склад не содержит необходимое количество товара'
                        + f' ({required_payload} > {val}).'
            )

        if not is_vehicle_available(
            vehicle=vehicle,
            date_start=date_start,
            date_end=date_end
        ):
            raise ValidationError(
                message='Машина в это время занята.'
            )
        raise ValidationError('asd')
        return cleaned_data

    class Meta:
        fields = (
            'date_start',
            'date_end',
            'payload',
            'product',
            'shop',
            'vehicle',
            'warehouse'
        )
        model = ProductShopOrder
