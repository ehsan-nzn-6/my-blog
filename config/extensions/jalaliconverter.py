from extensions.Jalali import Gregorian, Persian
from django.utils import timezone


def toPersian(date):
    # date = timezone.localtime(date)
    year = date.year
    if year % 10 == year:
        year = f"0{year}"
    month = date.month
    if month % 10 == month:
        month = f"0{month}"
    day = date.day
    if day % 10 == day:
        day = f"0{day}"
    hour = date.hour
    if hour % 10 == hour:
        hour = f"0{hour}"
    minute = date.minute
    if minute % 10 == minute:
        minute = f"0{minute}"
    second = date.second
    if second % 10 == second:
        second = f"0{second}"
    time = (date.hour, date.minute, date.second)
    out = Gregorian(f"{year},{month},{day}").persian_tuple()
    out = {
        "year": out[0],
        "month": out[1],
        "day": out[2],
        "hour": hour,
        "minute": minute,
        "second": second,
    }
    return out


def mydate():
    date = timezone.now()
    date = timezone.localtime(date)
    date = toPersian(date)
    return f"{date['year']}/{date['month']}/{date['day']} {date['hour']}:{date['minute']}:{date['second']}"
