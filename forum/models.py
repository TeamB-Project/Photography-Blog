from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class ForumTopic(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('forumtopic-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title

class ForumThread(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(ForumTopic, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50, default='untitled')
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forumthread-detail', kwargs={'pk': self.pk})

class ForumComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(ForumThread, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()

    def __str__(self):
        return self.body