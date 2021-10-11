from django.contrib import admin
from blog.models import Article, Category

admin.site.site_header = 'وبلاگ من'


@admin.action(description='انتشار مقالات انتخاب شده')
def make_published(modeladmin, request, queryset):
    row_updated = queryset.update(status='p')
    if row_updated == 1:
        message_bit = 'منتشر شد.'
    else:
        message_bit = f'منتشر شدند.'
    modeladmin.message_user(request, f'{row_updated} مقاله {message_bit}')


@admin.action(description='پیش نویس شدن مقالات انتخاب شده')
def make_draft(modeladmin, request, queryset):
    row_updated = queryset.update(status='d')
    if row_updated == 1:
        message_bit = 'پیش نویس شد.'
    else:
        message_bit = f'پیش نویس شدند.'
    modeladmin.message_user(request, f'{row_updated} مقاله {message_bit}')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent',  'status')
    list_filter = ('status',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'author', 'slug',
                    'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')
    actions = (make_published, make_draft)

    def category_to_str(self, obj):
        return '، '.join([category.title for category in obj.category.active()])
    category_to_str.short_description = 'دسته بندی'


admin.site.register(Article, ArticleAdmin)
