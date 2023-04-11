from datetime import datetime

from django.db.models import Sum
from django.forms import DateField, Form, ModelForm, ValidationError, CharField

from .models import (Product, ProductOrder, ProductTransit, ProductWarehouse,
                     Shop, Vehicle, VehicleOrder, VehicleTransit, Warehouse)
from .utils import (get_datetime_local_timezone, get_inline_sum,
                    get_product_payload_diff, is_vehicle_available)
from django.conf import settings


class ProductOrderInlineForm(ModelForm):
    """Inline entity attached to ProductOrder model. Used in Order instance."""
    def clean_payload(self):
        """
        Custom validation while creating new order for required payload --
        checks that count of this product will be in an associated warehouse at
        chosen time.
        """
        if self.data.get('warehouse') != '':
            product: Product = self.cleaned_data.get('product')
            required_payload: int = self.cleaned_data.get('payload')
            warehouse_id: int = self.data.get('warehouse')
            warehouse = Warehouse.objects.filter(pk=warehouse_id).first()

            date_start: str = self.data.get('date_start_0')
            time_start: str = self.data.get('date_start_1')
            date_end: str = self.data.get('date_end_0')
            time_end: str = self.data.get('date_end_1')

            if all(i for i in (date_start, time_start, date_end, time_end)):
                date_start: datetime = get_datetime_local_timezone(
                    date=date_start,
                    time=time_start
                )
                date_end: datetime = get_datetime_local_timezone(
                    date=date_end,
                    time=time_end
                )
                diff: int = get_product_payload_diff(
                    date_start=date_start,
                    product=product,
                    warehouse=warehouse
                )
                current_payload: int = ProductWarehouse.objects.filter(
                    product=product,
                    warehouse=warehouse
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
    """
    Inline entity attached to ProductTransit model. Used in Transit instance.
    """
    def clean(self):
        """
        Custom validation while creating new Transit -- checks if total new
        payload is less or equals to warehouse capacity.
        """
        cleaned_data = super().clean()

        if (warehouse_id := self.data.get('warehouse')) != '':
            warehouse: Warehouse = Warehouse.objects.get(pk=warehouse_id)
            new_payload: int = get_inline_sum(
                data=self.data,
                pattern=r'^product_transit-[0-9]+-payload$'
            )
            current_payload: int = ProductWarehouse.objects.filter(
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


class ProductWarehouseInlineForm(ModelForm):
    """
    Inline entity attached to ProductWarehouse model. Used in Warehouse
    instance.
    """
    def clean(self):
        """
        Custom validation while creating new Warehouse -- checks if total new
        payload is less or equals to warehouse capacity.
        """
        cleaned_data = super().clean()

        if (max_capacity := self.data.get('max_capacity')) != '':
            max_capacity = int(max_capacity)
            new_payload: int = get_inline_sum(
                data=self.data,
                pattern=r'^product_warehouse-[0-9]+-payload$'
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


class QueryDateForm(Form):
    date = DateField(label='Введите дату:')


class QueryFullnameForm(Form):
    first_name = CharField(
        max_length=settings.MAX_NAME_LENGTH,
        label='Введите имя:'
    )
    last_name = CharField(
        max_length=settings.MAX_NAME_LENGTH,
        label='Введите фамилию:'
    )


class QuerySixForm(QueryDateForm, QueryFullnameForm):
    pass


class QueryWarehouseNameForm(Form):
    name = CharField(
        max_length=settings.MAX_WAREHOUSE_NAME_LENGTH,
        label='Введите название:'
    )
    address = CharField(
        max_length=settings.MAX_ADDRESS_LENGTH,
        label='Введите адрес:'
    )


class ShopForm(ModelForm):
    """Form for Shop model."""
    def clean_name(self):
        """
        Custom validation while creating new shop -- checks that name is
        available.
        """
        name: str = self.cleaned_data.get('name')
        if Shop.objects.filter(name=name).exists():
            raise ValidationError(
                message='Магазин с таким названием уже существует.'
            )

        return name

    class Meta:
        fields = ('address', 'name', 'owner')
        model = Shop


class VehicleInlineBaseForm(ModelForm):
    """Base form for Vehicle inline instance."""
    def clean_vehicle(self):
        """
        Custom validation while creating instance that contains vehicle --
        checks that vehicle is available at given time range.
        """
        vehicle: Vehicle = self.cleaned_data.get('vehicle')
        date_start: str = self.data.get('date_start_0')
        time_start: str = self.data.get('date_start_1')
        date_end: str = self.data.get('date_end_0')
        time_end: str = self.data.get('date_end_1')

        if all(i for i in (date_start, time_start, date_end, time_end)):
            date_start: datetime = get_datetime_local_timezone(
                date=date_start,
                time=time_start
            )
            date_end: datetime = get_datetime_local_timezone(
                date=date_end,
                time=time_end
            )

            if not is_vehicle_available(
                date_end=date_end,
                date_start=date_start,
                vehicle=vehicle
            ):
                raise ValidationError(
                    message='Машина занята в это время.'
                )

        return vehicle

    class Meta:
        fields = ('vehicle',)


class VehicleOrderInlineForm(VehicleInlineBaseForm):
    """Inline entity attached to VehicleOrder model. Used in Order instance."""
    class Meta(VehicleInlineBaseForm.Meta):
        model = VehicleOrder


class VehicleTransitInlineForm(VehicleInlineBaseForm):
    """
    Inline entity attached to VehicleTransit model. Used in Transit instance.
    """
    class Meta(VehicleInlineBaseForm.Meta):
        model = VehicleTransit
