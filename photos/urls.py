from django.urls import path
from . import views
from .views import (
    addPhoto
)

urlpatterns = [
    path('gallery/', views.gallery, name='gallery'),
    path('viewphoto/<str:pk>/', views.viewPhoto, name='viewphoto'),
    path('add/', addPhoto.as_view(), name='add'),
    path('membergallery/<str:pid>/', views.membergallery, name='membergallery'),
    path('photo/update/success/', views.photo_update, name='photo-update-success'),
]