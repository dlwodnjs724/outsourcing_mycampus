from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.main, name="main"),
    path('register/', views.main_register, name='main_register'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('<str:url_name>/', include('core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
