from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.gallery, name='gallery'),
    path('viewphoto/<str:pk>/', views.viewPhoto, name='viewphoto'),
    path('add/', views.addPhoto, name='add'),
    path('membergallery/<str:pid>/', views.membergallery, name='membergallery'),
]