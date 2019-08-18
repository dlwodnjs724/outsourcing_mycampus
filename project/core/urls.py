from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
<<<<<<< HEAD
    path('<str:url_name>/', views.main, name="main")
=======
    path('', include('board.urls'))

>>>>>>> email
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
