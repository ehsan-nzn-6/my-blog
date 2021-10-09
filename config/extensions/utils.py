import jdatetime
from django.utils import timezone


def numbers_to_persian(mystr):
    persian_numbers = ('۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹')
    for i in range(10):
        mystr = mystr.replace(str(i), persian_numbers[i])
    return mystr


def datetime_to_shamsi(datetime):
    JMONTHS = (
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
    )
    publish_datetime = timezone.localtime(datetime)
    jdate_tuple = jdatetime.GregorianToJalali(
        publish_datetime.year, publish_datetime.month, publish_datetime.day).getJalaliList()
    output = f'{jdate_tuple[2]} {JMONTHS[jdate_tuple[1]-1]} {jdate_tuple[0]:02} | ساعت {publish_datetime.hour:02}:{publish_datetime.minute:02}'
    output = numbers_to_persian(output)
    return output
