from django.urls import path
from django.conf import settings
from account.views import *
from django.conf.urls.static import static

app_name = 'auth'

urlpatterns = [
    # 
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)