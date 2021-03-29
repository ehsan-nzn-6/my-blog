from django import forms
from .models import DakhlOKharj


class DakhlOKharjForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DakhlOKharjForm, self).__init__(*args, **kwargs)
        # self.fields["user"].widget = forms.HiddenInput()

    class Meta:
        model = DakhlOKharj
        fields = "__all__"