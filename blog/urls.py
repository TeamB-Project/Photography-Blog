from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    SearchResultsView
)
from . import views
from photos.views import membergallery

urlpatterns = [
    path('articles/', PostListView.as_view(), name='blog-articles'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('forum/', views.forum, name='blog-forum'),
    path('howto/', views.howto, name='blog-howto'),
    path('other/', views.other, name='blog-other'),
    path('tips&tricks/', views.tipstricks, name='blog-tipstricks'),
    path('reviews/', views.reviews, name='blog-reviews'),
    path('', views.home, name='blog-home'),
    path('home/', views.home, name='home'),
    path('post/delete/success/', views.post_delete, name='post-delete-success'),
    path('post/update/success/', views.post_update, name='post-update-success'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('membergallery/<str:pid>/', membergallery, name='membergallery'),
]