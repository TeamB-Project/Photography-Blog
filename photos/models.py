from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from taggit.managers import TaggableManager

class PhotoCategory(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    description = models.CharField(max_length=300,null=False,blank=False)

    def __str__(self):
        return self.name

class Photo(models.Model):
    photocategory = models.ForeignKey(PhotoCategory, on_delete=models.SET_NULL,null=True,blank=False)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    photographer = models.ForeignKey(User,on_delete=models.CASCADE)
    publishdate = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    location = models.CharField(max_length=100, null=True,blank=True)
    camera = models.CharField(max_length=80, null=True,blank=True)
    focal = models.CharField(max_length=10, null=True,blank=True)
    aperture = models.CharField(max_length=15, null=True,blank=True)
    shutter = models.CharField(max_length=20, null=True,blank=True)
    iso = models.CharField(max_length=20, null=True,blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.description + '------' + str(self.approved)