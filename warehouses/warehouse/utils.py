import re
from datetime import datetime as dt, timedelta, timezone
from warehouses.settings import TIMEZONE_OFFSET


def get_inline_sum(pattern: str, data: dict[str, str]) -> int:
    res = 0
    for key, val in data.items():
        if re.match(pattern, key):
            res += int(val)

    return res


def get_now_datetime():
    return dt.now(tz=timezone(offset=timedelta(hours=TIMEZONE_OFFSET)))
