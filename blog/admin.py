from django.contrib import admin
from .models import Post, Category, BlogComment
from django.db import models
import datetime

admin.site.register(Category)
admin.site.register(BlogComment)

@admin.action(description='Publish selected posts')
def publish(modeladmin, request, queryset):
    current_datetime = datetime.datetime.now()  
    queryset.update(approved = 'True', date_posted = current_datetime)

@admin.action(description='Unpublish selected posts')
def unpublish(modeladmin, request, queryset):
    queryset.update(approved = 'False', date_posted = None)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'approved', 'content', 'date_posted', 'author', 'category', 'tag_list']
    actions = [publish, unpublish]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())