import datetime
import time


def datetime_to_timestamp(dt: str) -> int:
    """将时间字符串转换为时间戳"""

    dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(dt.timetuple()))
    return timestamp
