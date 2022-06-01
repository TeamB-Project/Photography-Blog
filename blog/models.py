from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default='uncategorized')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    tags = TaggableManager()
    approved = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + '------' + str(self.author) + '------' + str(self.date_posted)

    def get_absolute_url(self):
        return reverse('blog-articles')

    #def get_absolute_url(self):
        #return reverse('post-detail',kwargs={'pk': self.pk})

class Category(models.Model): 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog-articles')

class BlogComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()

    def __str__(self):
        return self.body