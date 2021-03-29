from django.db import models
from django.urls import reverse
from account.models import MyUser
from django.utils import timezone
from extensions.jalaliconverter import toPersian, mydate


class DakhlOKharj(models.Model):
    text = models.CharField(max_length=100)
    date = models.CharField(max_length=50, default=mydate, null=True, blank=True)
    amount = models.FloatField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    kharj = models.BooleanField(default=True)

    def __str__(self):
        return str(self.text)

    def get_absolute_url(self):
        return reverse("dakhlokharj:DakhlOKharjList")  # , kwargs={"pk": self.pk}

    def camount(self):  # with cama
        return f"{self.amount:,}"

    def jdate(self):
        date = toPersian(self.date)
        return f"{date['year']}/{date['month']}/{date['day']} {date['hour']}:{date['minute']}:{date['second']}"
