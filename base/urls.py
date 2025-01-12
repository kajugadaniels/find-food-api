from django.urls import path
from django.conf import settings
from base.views import *
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('categories/', getCategories.as_view(), name='getCategories'),
    path('category/add/', addCategory.as_view(), name='addCategory'),
    path('category/<slug>/', showCategory.as_view(), name='showCategory'),
    path('category/<slug>/edit/', editCategory.as_view(), name='editCategory'),
    path('category/<slug>/delete/', deleteCategory.as_view(), name='deleteCategory'),

    path('places/', getPlaces.as_view(), name='getPlaces'),
    path('place/add/', addPlace.as_view(), name='addPlace'),
    path('place/<slug>/', showPlace.as_view(), name='showPlace'),
    path('place/<slug>/edit/', editPlace.as_view(), name='editPlace'),
    path('place/<slug>/delete/', deletePlace.as_view(), name='deletePlace'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)