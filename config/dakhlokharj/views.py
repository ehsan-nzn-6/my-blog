from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DakhlOKharj
from account.models import MyUser
from account.mixins import (
    FieldsMixin,
    FormValidMixin,
    AccessMixin,
    DeleteBudgethandlerMixin,
    UpdateBudgethandlerMixin,
)
from django.urls import reverse_lazy

# Create your views here.
class DakhlOKharjListView(LoginRequiredMixin, ListView):
    model = DakhlOKharj

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DakhlOKharj.objects.all()
        else:
            return DakhlOKharj.objects.filter(user=self.request.user).order_by("-date")


class DakhlOKharjCreateView(
    LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateView
):
    template_name = "./dakhlokharj/dakhlokharj_create.html"
    model = DakhlOKharj


class DakhlOKharjUpdateView(
    LoginRequiredMixin, FieldsMixin, UpdateBudgethandlerMixin, AccessMixin, UpdateView
):
    template_name = "./dakhlokharj/dakhlokharj_create.html"
    model = DakhlOKharj
    fields = "__all__"


class DakhlOKharjDeleteView(
    LoginRequiredMixin, AccessMixin, DeleteBudgethandlerMixin, DeleteView
):
    model = DakhlOKharj
    success_url = reverse_lazy("dakhlokharj:DakhlOKharjList")
