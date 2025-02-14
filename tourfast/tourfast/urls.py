from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import profile, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('profile', profile, name="profile"),
    path('register', RegisterView.as_view(), name="register"),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
