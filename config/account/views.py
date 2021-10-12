from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Article
from account.mixins import *
from django.urls import reverse_lazy
# @login_required
# def home(request):
#     return render(request, 'registration/home.html')


class ArticleList(LoginRequiredMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        # customize query
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FormValidMixins, FieldsMixins, CreateView):
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
