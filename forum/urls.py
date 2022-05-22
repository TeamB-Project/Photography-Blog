from django.contrib import admin
from django.urls import path

from .views import (
    ForumTopicCreateView,
    ForumTopicListView,
    ForumTopicDetailView,
    ForumThreadCreateView,
    ForumThreadDetailView,
    ForumThreadUpdateView,
    ForumThreadDeleteView,
    ForumCommentDeleteView
)

urlpatterns = [
    path('discussion/', ForumTopicListView.as_view(), name='discussion'),
    path('forumtopic/add/', ForumTopicCreateView.as_view(), name='forumtopic-add'),
    path('forumtopic/<int:pk>/', ForumTopicDetailView.as_view(), name='forumtopic-detail'),
    path('forumtopic/<int:pk>/newpost/', ForumThreadCreateView.as_view(), name='forumthread-create'),
    path('forumthread/<int:pk>/', ForumThreadDetailView.as_view(), name='forumthread-detail'),
    path('forumthread/<int:pk>/update/', ForumThreadUpdateView.as_view(), name='forumthread-update'),
    path('forumthread/<int:pk>/delete/', ForumThreadDeleteView.as_view(), name='forumthread-delete'),
    path('forumcomment/<int:pk>/delete/', ForumCommentDeleteView.as_view(), name='forumcomment-delete'),
]