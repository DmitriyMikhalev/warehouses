import re
from datetime import datetime as dt, timedelta, timezone
from warehouses.settings import TIMEZONE_OFFSET
from django.apps import apps


def get_inline_sum(pattern: str, data: dict[str, str]) -> int:
    res = 0
    for key, val in data.items():
        if re.match(pattern, key):
            res += int(val) or 0

    return res


def get_now_datetime():
    return dt.now(tz=timezone(offset=timedelta(hours=TIMEZONE_OFFSET)))


def is_correct_timerange(start_1, end_1, start_2, end_2) -> bool:
    return end_1 < start_2 or start_1 > end_2


def is_vehicle_available(vehicle, date_start, date_end):
    VehicleTransit = apps.get_model('warehouse', 'VehicleTransit')
    Order = apps.get_model('warehouse', 'Order')

    for obj in VehicleTransit.objects.filter(
        vehicle=vehicle,
        transit__date_start__gte=date_start - timedelta(days=1),
        transit__date_end__lte=date_end + timedelta(days=1)
    ):
        if not is_correct_timerange(
            start_1=obj.transit.date_start,
            end_1=obj.transit.date_end,
            start_2=date_start,
            end_2=date_end
        ):
            return False
    print('ne bilo')
    for order in Order.objects.filter(
        vehicle=vehicle,
        date_start__gte=date_start - timedelta(days=1),
        date_end__lte=date_end + timedelta(days=1)
    ):
        if not is_correct_timerange(
            start_1=order.date_start,
            end_1=order.date_end,
            start_2=date_start,
            end_2=date_end
        ):
            return False

    return True


def get_inline_objs_id(pattern: str, data: dict[str, str]) -> list:
    res = []
    for key, val in data.items():
        if re.match(pattern, key):
            res.append(val)

    return res
