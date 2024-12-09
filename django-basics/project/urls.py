
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('',include('recipes.urls')),
    path('auth/',include('authors.urls')),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls()


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)