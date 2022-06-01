from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Category,BlogComment
from django.views.generic.edit import FormMixin
from .forms import (PostForm, UpdateForm, BlogCreateCommentForm)
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from taggit.models import Tag

def home(request):
    return render(request, 'blog/home.html')

def articles(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/articles.html', context)

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/articles.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'

    def get_queryset(self):
        currenttime = timezone.now()
        return Post.objects.filter(Q(date_posted__isnull=False),Q(date_posted__lt=currenttime)).order_by('-date_posted')

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = BlogCreateCommentForm

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        context['blogcomments'] = BlogComment.objects.filter(post=self.kwargs.get('pk')).order_by('-timestamp')
        context['form'] = BlogCreateCommentForm(initial={'post': self.object, 'author': self.request.user})
        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'blog/update_post_form.html'
    success_url = reverse_lazy('post-update-success')

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
    success_url = reverse_lazy('post-delete-success')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def gallery(request):
    return render(request, 'blog/gallery.html', {'title': 'Gallery'})

def forum(request):
    return render(request, 'blog/forum.html', {'title': 'Forum'})

def howto(request):
    return render(request, 'blog/howto.html', {'title': 'How-to...'})

def tipstricks(request):
    return render(request, 'blog/tipstricks.html', {'title': 'Tips&Tricks'})

def reviews(request):
    return render(request, 'blog/reviews.html', {'title': 'Camera&LensReviews'})

def other(request):
    return render(request, 'blog/other.html', {'title': 'Other'})

def post_delete(request):
    return render(request, 'blog/post_delete_success.html', {'title': 'Article Deleted'})

def post_update(request):
    return render(request, 'blog/post_update_success.html', {'title': 'Article Updated'})

class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/articles.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get("post-search")
        object_list = Post.objects.filter(
            Q(title__icontains=query) & Q(date_posted__isnull=False)
        ).exclude(Q(title__iexact='')).order_by('-date_posted')
        return object_list

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['posts'] = Post.objects.all()
        context['toptags'] = Post.tags.most_common()[:10]
        return context

class TagIndexView(TagMixin, ListView):
    model = Post
    template_name = 'blog/articles.html'

    def get_context_data(self, **kwargs):
            context = super(TagMixin, self).get_context_data(**kwargs)
            context['tags'] = Tag.objects.all()
            context['allposts'] = Post.objects.all()
            context['toptags'] = Post.tags.most_common()[:10]
            context['posts'] = Post.objects.filter(Q(tags__slug=self.kwargs.get('tag_slug')),Q(approved=True))
            return context