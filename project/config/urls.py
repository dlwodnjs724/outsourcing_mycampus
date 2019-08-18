from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.main, name="main"),
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('core.urls')),
    path('board/<str:univ>/', include('board.urls')),
    path('auth/', include('accounts.urls'))

=======
    path('api/', include('api.urls')),
    path('auth/', include('accounts.urls')),
    path('<str:url_name>/', include('core.urls')),
>>>>>>> email
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('debug', include(debug_toolbar.urls)),
    ]
