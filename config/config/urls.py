
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from account.views import LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('account.urls')),
    path('', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='login'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
