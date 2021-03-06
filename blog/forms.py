from django import forms
from .models import Post, Category, BlogComment
from taggit.forms import TagWidget

categories = Category.objects.all().values_list('name','name')


categories_list = []


for item in categories:
    categories_list.append(item)

 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'author', 'content', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control','value':'','id':'uid','type':'hidden'}),
            'category': forms.Select(choices=categories_list, attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=categories_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': TagWidget(),
        }

class BlogCreateCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['body', 'author', 'post']