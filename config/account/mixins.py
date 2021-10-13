from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article


class FieldsMixins():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ('title', 'slug', 'category',
                       'description', 'thumbnail', 'publish', 'is_special', 'status')
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


class FormValidMixins():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixins():
    # users cant edit others article
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user or request.user.is_superuser or article.status in ['d', 'b']:
            # goto response
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class SuperuserAccessMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            # goto response
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class AuthorsMixins():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                # goto response
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('account:profile')
        else:
            return redirect('login')
