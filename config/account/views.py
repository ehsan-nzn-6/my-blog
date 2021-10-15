from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignupForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Article
from account.mixins import *
from django.urls import reverse_lazy
from account.models import User
from account.forms import ProfileForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import views

# @login_required
# def home(request):
#     return render(request, 'registration/home.html')


class ArticleList(AuthorsMixins, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        # customize query
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(AuthorsMixins, FormValidMixins, FieldsMixins, CreateView):
    model = Article
    # its handled on mixins
    # fields = ('author', 'title', 'slug', 'category',
    #           'description', 'thumbnail', 'publish', 'status')
    template_name = 'registration/article_create_update.html'


class ArticleUpdate(AuthorAccessMixins, FormValidMixins, FieldsMixins, UpdateView):
    model = Article
    # its handled on mixins
    # fields = ('author', 'title', 'slug', 'category',
    #           'description', 'thumbnail', 'publish', 'status')
    template_name = 'registration/article_create_update.html'


class ArticleDelete(SuperuserAccessMixins, DeleteView):
    model = Article
    template_name = 'registration/article_confirm_delete.html'
    success_url = reverse_lazy('account:home')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')
    template_name = 'registration/profile.html'

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        # add some kwargs
        # send user to form
        kwargs = super(ProfileUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class LoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت.'
        message = render_to_string('registration/activate_account.html', {
            # context of that template
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد <a href="/login">ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('account:login')
        return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود <a href="/login">کلیک</a> کنید. ')
    else:
        return HttpResponse('لینک فعالسازی منقضی شده است. <a href="/login">دوباره امتحان کنید</a>')
