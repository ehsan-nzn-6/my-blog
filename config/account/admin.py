from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

UserAdmin.fieldsets[1][1]["fields"] = ("first_name", "last_name", "email", "budget")


admin.site.register(MyUser, UserAdmin)
