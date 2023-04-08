import re
from zoneinfo import ZoneInfo
from datetime import datetime as dt
from django.db.models import Sum
from django.apps import apps
from django.conf import settings


def get_inline_sum(pattern: str, data: dict[str, str]) -> int:
    res = 0
    for key, val in data.items():
        if re.match(pattern, key) and val != '':
            res += int(val)

    return res


def get_now_datetime():
    return dt.now(tz=ZoneInfo(key=settings.TIME_ZONE))


def get_datetime_local_timezone(date, time):
    return dt.strptime(
            date + ' ' + time,
            '%d.%m.%Y %H:%M:%S'
        ).replace(tzinfo=ZoneInfo(key=settings.TIME_ZONE))


def is_correct_timerange(start_1, end_1, start_2, end_2) -> bool:
    return end_1 < start_2 or start_1 > end_2


def is_vehicle_available(vehicle, date_start, date_end):
    VehicleTransit = apps.get_model('warehouse', 'VehicleTransit')
    VehicleOrder = apps.get_model('warehouse', 'VehicleOrder')

    for obj in VehicleTransit.objects.filter(
        vehicle=vehicle,
        transit__date_start__lte=date_end,
        transit__date_end__gte=date_start,
        transit__accepted=False
    ):
        if not is_correct_timerange(
            start_1=obj.transit.date_start,
            end_1=obj.transit.date_end,
            start_2=date_start,
            end_2=date_end
        ):
            print(repr(obj))
            return False

    for obj in VehicleOrder.objects.filter(
        vehicle=vehicle,
        order__date_start__lte=date_end,
        order__date_end__gte=date_start,
        order__accepted=False
    ):
        if not is_correct_timerange(
            start_1=obj.order.date_start,
            end_1=obj.order.date_end,
            start_2=date_start,
            end_2=date_end
        ):
            return False

    return True


def get_inline_objs_id(pattern: str, data: dict[str, str]) -> list[int]:
    res = []
    for key, val in data.items():
        if re.match(pattern, key) and val != '':
            res.append(int(val))

    return res


def has_inline_duplicates(pattern: str, data: dict[str, str]):
    obj_ids = get_inline_objs_id(
            pattern=pattern,
            data=data
        )

    return len(set(obj_ids)) != len(obj_ids)


def get_product_payload_diff(warehouse, product, date_start) -> int:
    ProductTransit = apps.get_model('warehouse', 'ProductTransit')
    ProductOrder = apps.get_model('warehouse', 'ProductOrder')

    negative_payload = ProductOrder.objects.filter(
        order__accepted=False,
        product=product,
        order__warehouse=warehouse,
        order__date_start__gte=get_now_datetime(),
        order__date_end__lt=date_start
    ).aggregate(sum=Sum('payload')).get('sum') or 0

    positive_payload = ProductTransit.objects.filter(
        transit__accepted=False,
        product=product,
        transit__warehouse=warehouse,
        transit__date_start__gte=get_now_datetime(),
        transit__date_end__lt=date_start,
    ).aggregate(sum=Sum('payload')).get('sum') or 0

    return positive_payload - negative_payload


def get_diff_order(order) -> dict[int, int]:
    return {obj.product: obj.payload for obj in order.product_order.all()}


def get_diff_transit(transit) -> dict[int, int]:
    return {obj.product: obj.payload for obj in transit.product_transit.all()}
