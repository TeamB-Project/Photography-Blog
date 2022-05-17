from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import ForumTopic, ForumThread, ForumComment
from .forms import ForumCreateCommentForm

# Topic views

class ForumTopicListView(ListView):
    model = ForumTopic
    template_name = 'forum/forum.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'forumtopics'

class ForumTopicDetailView(DetailView):
    model = ForumTopic

    def get_context_data(self, **kwargs):
        context = super(ForumTopicDetailView, self).get_context_data(**kwargs)
        context['forumthreads'] = ForumThread.objects.filter(topic=self.kwargs.get('pk')).order_by('-timestamp')
        return context

class ForumTopicCreateView(LoginRequiredMixin, CreateView):
    model = ForumTopic
    fields = ['title', 'description']

    def form_valid(self, form):
        return super().form_valid(form)

# Thread views

class ForumThreadDetailView(FormMixin, DetailView):
    model = ForumThread
    form_class = ForumCreateCommentForm

    def get_context_data(self, **kwargs):
        context = super(ForumThreadDetailView, self).get_context_data(**kwargs)
        context['forumcomments'] = ForumComment.objects.filter(post=self.kwargs.get('pk')).order_by('-timestamp')
        context['form'] = ForumCreateCommentForm(initial={'post': self.object, 'author': self.request.user})

        return context

    def get_success_url(self):
        return reverse('forumthread-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ForumThreadDetailView, self).form_valid(form)

class ForumThreadCreateView(LoginRequiredMixin, CreateView):
    model = ForumThread
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = ForumTopic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

class ForumThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ForumThread
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ForumThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ForumThread
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    

# Static pages

def login(request):
    return render(request, 'forum/login.html')

def logout(request):
    return render(request, 'forum/logout.html')