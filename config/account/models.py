from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_author = models.BooleanField(
        default=False, verbose_name='وضعیت نویسنده')
    special_user = models.DateTimeField(
        default=timezone.now, verbose_name='کاربر ویژه تا')

    def is_special_user(self):
        if timezone.now() < self.special_user:
            return True
        return False
    is_special_user.boolean = True  # look prettier in admin page like bool x
    is_special_user.short_description = 'وضعیت کاربر ویژه'
