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


# class PasswordChangeView(views.PasswordChangeView):
#     success_url = reverse_lazy('account:password_change_done')
