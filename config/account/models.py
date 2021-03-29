from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    budget = models.FloatField(default=0)

    def cbudget(self):  # with cama
        return f"{self.budget:,}"
