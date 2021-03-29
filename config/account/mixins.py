from django.http import Http404
from account.models import MyUser
from dakhlokharj.models import DakhlOKharj


class FieldsMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["text", "date", "amount", "kharj", "user"]
        elif request.user.is_superuser == False:
            self.fields = ["text", "date", "amount", "kharj"]
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class AccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        dakhlokharj = DakhlOKharj.objects.get(pk=pk)
        if request.user != dakhlokharj.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    def budget_handler(self, form):
        user = self.request.user
        setbudgetObj = MyUser.objects.get(username=user)
        if form.cleaned_data["kharj"] == True:
            setbudgetObj.budget -= form.cleaned_data["amount"]
        else:
            setbudgetObj.budget += form.cleaned_data["amount"]
        setbudgetObj.save()

    def form_valid(self, form):
        if self.request.user.is_superuser:
            self.budget_handler(form)
            form.save()
        else:
            self.budget_handler(form)
            self.obj = form.save(commit=False)
            self.obj.user = self.request.user
        return super().form_valid(form)


"""BUDGET HANDLERS:"""


class DeleteBudgethandlerMixin:
    def budget_handler(self, request, *args, **kwargs):
        user = self.request.user
        obj = DakhlOKharj.objects.get(pk=self.kwargs["pk"])
        setbudgetObj = MyUser.objects.get(username=user)
        if obj.kharj:
            setbudgetObj.budget += (
                obj.amount / 2
            )  # Reverse # /2 for two time runned handler, because ar u sure question
        else:
            setbudgetObj.budget -= obj.amount / 2
        setbudgetObj.save()
        # user.save()

    def dispatch(self, request, *args, **kwargs):
        dakhlokharj = DakhlOKharj.objects.get(pk=self.kwargs["pk"])
        self.budget_handler(request)
        if request.user != dakhlokharj.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class UpdateBudgethandlerMixin(FormValidMixin):
    def budget_handler(self, form, *args, **kwargs):
        user = self.request.user
        obj = DakhlOKharj.objects.get(pk=self.kwargs["pk"])
        current_amount = obj.amount
        new_amount = form.cleaned_data["amount"]
        most_include = current_amount - new_amount  # -1 = 3 - 4
        setbudgetObj = MyUser.objects.get(username=user)

        # Reverse # /2 for two time runned handler, because ar u sure question
        if obj.kharj:
            setbudgetObj.budget += most_include
        else:
            setbudgetObj.budget -= most_include

        setbudgetObj.save()
