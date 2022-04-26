from django.contrib import admin
from .models import PhotoCategory, Photo
from django.db import models
import datetime

admin.site.register(PhotoCategory)

@admin.action(description='Publish selected photos')
def publish(modeladmin, request, queryset):
    current_datetime = datetime.datetime.now()  
    queryset.update(approved = 'True', publishdate = current_datetime)

@admin.action(description='Unpublish selected photos')
def unpublish(modeladmin, request, queryset):
    queryset.update(approved = 'False', publishdate = None)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['image', 'approved', 'photocategory', 'publishdate', 'tag_list', 'photographer', 'location', 'description']
    actions = [publish, unpublish]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

