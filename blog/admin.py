from django.contrib import admin
from .models import Post, Category, BlogComment
from django.db import models
import datetime

admin.site.register(Category)
admin.site.register(BlogComment)

@admin.action(description='Publish selected posts')
def publish(modeladmin, request, queryset):
    current_datetime = datetime.datetime.now()  
    queryset.update(date_posted = current_datetime)

@admin.action(description='Unpublish selected posts')
def unpublish(modeladmin, request, queryset):
    queryset.update(date_posted = None)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'date_posted', 'author', 'category']
    actions = [publish, unpublish]