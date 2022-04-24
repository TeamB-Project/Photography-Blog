from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class PhotoCategory(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    photocategory = models.ForeignKey(PhotoCategory, on_delete=models.SET_NULL,null=True,blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    photographer = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    publishdate = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    location = models.CharField(max_length=100, null=True,blank=True)

    def __str__(self):
        return self.description + '------' + str(self.approved)