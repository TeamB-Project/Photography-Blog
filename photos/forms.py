from django import forms
from .models import Photo

class PhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('approved', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }