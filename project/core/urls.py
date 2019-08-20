from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
    path("auth/", include("accounts.urls")),
    path('', include('board.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
