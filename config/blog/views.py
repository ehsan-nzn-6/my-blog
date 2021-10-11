from django.core import paginator
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Article, Category
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from account.models import User


# def home(request, page=1):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 5)
#     # page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         'articles': articles,
#     }
#     return render(request, 'blog/home.html', context)
class ArticleList(ListView):
    # model = Article
    # template_name = 'blog/home.html'
    # context_object_name = 'articles'
    queryset = Article.objects.published()
    paginate_by = 3


# def detail(request, slug):
#     context = {
#         # Article.objects.get(slug=slug)
#         'article': get_object_or_404(Article.objects.published(), slug=slug, status='p'),
#     }
#     return render(request, 'blog/detail.html', context)
class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 5)
#     # page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles,
#     }
#     return render(request, 'blog/category.html', context)
class CategoryList(ListView):
    paginate_by = 3
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        # use your custom queryset
        slug = self.kwargs.get('slug')
        self.category = get_object_or_404(Category.objects.active(), slug=slug)
        return self.category.articles.published()

    def get_context_data(self, **kwargs):
        # add some extra context
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class AuthorList(ListView):
    paginate_by = 3
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        # use your custom queryset
        username = self.kwargs.get('username')
        self.author = get_object_or_404(
            User, username=username)
        return self.author.articles.published()

    def get_context_data(self, **kwargs):
        # add some extra context
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context
