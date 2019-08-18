from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views
urlpatterns = [
    path('<str:url_name>/', views.main, name="main")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
