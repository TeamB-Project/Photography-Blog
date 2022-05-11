from django.contrib import admin
from .models import Profile
from django.db import models
import datetime

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'about', 'id', 'user_id']