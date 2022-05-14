from django.contrib import admin
from .models import ForumTopic, ForumThread, ForumComment

admin.site.register(ForumTopic)
admin.site.register(ForumThread)
admin.site.register(ForumComment)