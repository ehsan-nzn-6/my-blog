from django.db import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from blog.models import Article
# Create your views here.


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


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('author', 'title', 'slug', 'category',
              'description', 'thumbnail', 'publish', 'status')
    template_name = 'registration/article_create_update.html'
