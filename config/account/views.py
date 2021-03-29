from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView


class CreateAccount(CreateView):
    form_class = UserCreationForm
    template_name = "registration/create_account.html"

    def form_valid(self, form):
        user = form.save()
        user.save()
        return redirect("account:login")
