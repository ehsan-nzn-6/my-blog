
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from account.views import LoginView, Register, activate
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('account.urls')),
    path('', include('django.contrib.auth.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('comment/', include('comment.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
