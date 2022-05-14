from django import forms
from .models import ForumComment, ForumTopic

class ForumCreateTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'description']

class ForumCreateCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['body', 'author', 'post']