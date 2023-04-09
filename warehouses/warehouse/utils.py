import re
from zoneinfo import ZoneInfo
from datetime import datetime as dt
from django.db.models import Sum
from django.apps import apps
from django.conf import settings
from typing import Any


def get_datetime_local_timezone(date: str, time: str) -> dt:
    """
    Get datetime in local timezone using representations of date and time as a
    str. Time zone is defined at settings.py by TIME_ZONE.

    If date is specified as '13.04.2023', time as '13:42:58' and time zone
    offset is +05:00 UTC it will return '2023-04-13 13:42:58+05:00' that is
    str representation of datetime.datetime.
    """
    return dt.strptime(
            date + ' ' + time,
            '%d.%m.%Y %H:%M:%S'
        ).replace(tzinfo=ZoneInfo(key=settings.TIME_ZONE))


def get_diff_order(order) -> dict[Any, int]:
    """
    Returns dictionary with products and payloads connected to given order.

    For example, if order has 2 products with their ID's as str representation
    like '3' with 3 tons and '5' with 1 ton it will return
    {
        '3': 3,
        '5': 1,
    }
    """
    return {obj.product: obj.payload for obj in order.product_order.all()}


def get_diff_transit(transit) -> dict[Any, int]:
    """
    Returns dictionary with products and payloads connected to given transit.

    For example, if transit has 2 products with their ID's as str
    representation like '1' with 4 tons and '2' with 2 tons it will return
    {
        '1': 4,
        '2': 2,
    }
    """
    return {obj.product: obj.payload for obj in transit.product_transit.all()}


def get_inline_objs_id(pattern: str, data: dict[str, str]) -> list[int]:
    """
    Get a list of values casted to int from the specified dictionary
    whose keys correspond to the passed regular expression and values are not
    empty strs.

    For example, if regexp is '$[0-9]{1}d^' and data is
    {
        '1d': '3',
        '2d': '4',
        '33': '7',
        'd': '6',
        '0d': ''
    }
    it will return [3, 4].
    """
    res = []
    for key, val in data.items():
        if re.match(pattern, key) and val != '':
            res.append(int(val))

    return res


def get_inline_sum(pattern: str, data: dict[str, str]) -> int:
    """
    Get a sum of values casted to int from the specified dictionary
    whose keys correspond to the passed regular expression and values are not
    empty strs.

    For example, if regexp is '$[0-9]{1}d^' and data is
    {
        '1d': '3',
        '2d': '4',
        '33': '7',
        'd': '6',
        '0d': ''
    }
    it will return 3 + 4 = 7.
    """
    res = 0
    for key, val in data.items():
        if re.match(pattern, key) and val != '':
            res += int(val)

    return res


def get_now_datetime() -> dt:
    """
    Get datetime.now() with local timezone defined at settings.TIME_ZONE.
    """
    return dt.now(tz=ZoneInfo(key=settings.TIME_ZONE))


def get_product_payload_diff(warehouse, product, datetime: dt) -> int:
    """
    Returns the difference of product's count in given warehouse after transits
    and exportations made after now and before given datetime.

    For example, if some product in the given warehouse will be delivered
    in the amount of 3 and 5 tons and exported in the amount of 2 tons before
    the specified date it will return 3 + 5 - 2 = 6.
    """
    ProductTransit = apps.get_model('warehouse', 'ProductTransit')
    ProductOrder = apps.get_model('warehouse', 'ProductOrder')

    negative_payload: int = ProductOrder.objects.filter(
        order__accepted=False,
        product=product,
        order__warehouse=warehouse,
        order__date_start__gte=get_now_datetime(),
        order__date_end__lt=datetime
    ).aggregate(sum=Sum('payload')).get('sum') or 0

    positive_payload: int = ProductTransit.objects.filter(
        transit__accepted=False,
        product=product,
        transit__warehouse=warehouse,
        transit__date_start__gte=get_now_datetime(),
        transit__date_end__lt=datetime,
    ).aggregate(sum=Sum('payload')).get('sum') or 0

    return positive_payload - negative_payload


def has_inline_duplicates(pattern: str, data: dict[str, str]) -> bool:
    """
    Returns boolean value that is answer to the question 'is given dictionary
    has duplicate values attached to keys that matches given pattern?'.
    """
    obj_ids = get_inline_objs_id(
            data=data,
            pattern=pattern
        )

    return len(set(obj_ids)) != len(obj_ids)


def is_correct_timerange(start_1: dt, end_1: dt, start_2: dt,
                         end_2: dt) -> bool:
    """
    Returns boolean value that is answer to the question 'are given datetimes
    ranges have intersections?'. There is no matter which range is higher.
    If different bounds are equal it means case is incorrect.

    If one time range is presented as [] symbols that means start and end and
    other one is presented as {}, all combinations are:
        * [] {}  --> True
        * [ {] } --> False
        * { [] } --> False
        * { [} ] --> False
        * {} []  --> True
        * [ {} ] --> False

    Start of 1st range have to be higher that end of 2nd range or end of 1st
    range have to be lower than start of 2nd range.
    """
    return end_1 < start_2 or start_1 > end_2


def is_vehicle_available(vehicle, date_start: dt, date_end: dt) -> bool:
    """
    Returns boolean value that is answer to the question 'are given vehicle
    available at given time range?'.
    """
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
