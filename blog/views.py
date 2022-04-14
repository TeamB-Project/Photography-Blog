from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from blog.models import Post, Category
from .forms import (PostForm, UpdateForm) #forms.py


def home(request):
    return render(request, 'blog/home.html')


def articles(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/articles.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/articles.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'blog/update_post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def gallery(request):
    return render(request, 'blog/gallery.html', {'title': 'Gallery'}) #view gallery page

def forum(request):
    return render(request, 'blog/forum.html', {'title': 'Forum'}) #view forum page

def howto(request):
    return render(request, 'blog/howto.html', {'title': 'How-to...'}) #view how-too...

def tipstricks(request):
    return render(request, 'blog/tipstricks.html', {'title': 'Tips&Tricks'}) #tips&tricks

def reviews(request):
    return render(request, 'blog/reviews.html', {'title': 'Camera&LensReviews'}) #reviews