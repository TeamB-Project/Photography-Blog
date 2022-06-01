from django.urls import path
from . import views
from .views import (
    addPhoto,
    PhotoPostUpdateView,
    PhotoDetailView,
    PhotoLikeView
)

urlpatterns = [
    path('gallery/', views.gallery, name='gallery'),
    path('viewphoto/<str:pk>/', PhotoDetailView.as_view(), name='viewphoto'),
    path('add/', addPhoto.as_view(), name='add'),
    path('membergallery/<str:pid>/', views.membergallery, name='membergallery'),
    path('photo/update/success/', views.photo_update, name='photo-update-success'),
    path('tags/<slug:tag_slug>/', views.TagIndexView.as_view(), name='photos-by-tag'),
    path('viewphoto/<str:pk>/update/', PhotoPostUpdateView.as_view(), name='photo-update'),
    path('photolike<int:pk>', PhotoLikeView, name='like_photo'),
]