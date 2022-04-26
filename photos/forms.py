from distutils.command.upload import upload
from django import forms
from .models import Photo, PhotoCategory
 
photocategories = PhotoCategory.objects.all().values_list('name','name')

photocategories_list = []
for item in photocategories:
    photocategories_list.append(item)

class PhotoPostForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photocategory', 'description' , 'photographer', 'location', 'image', 'tags')
 
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'photographer': forms.TextInput(attrs={'class': 'form-control','value':'','id':'uid','type':'hidden'}),
            'photocategory': forms.Select(choices=photocategories_list, attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('description', 'photocategory', 'location','image')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'photocategory': forms.Select(choices=photocategories_list, attrs={'class': 'form-control'}),
            }