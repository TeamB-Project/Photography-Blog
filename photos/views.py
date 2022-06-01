from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, PhotoCategory
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import (PhotoPostForm, PhotoUpdateForm, PhotoCreateCommentForm )
from django.views.generic.edit import FormMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView
)
from django.urls import reverse_lazy, reverse
from taggit.models import Tag
from django.http import HttpResponseRedirect

def gallery(request):
    photocategory = request.GET.get('photocategory')
    if photocategory == None:
       photos = Photo.objects.filter(approved=True).order_by('-publishdate')
       photoset = "allphotos"
    else:
        photos = Photo.objects.filter(Q(photocategory__name=photocategory),Q(approved=True)).order_by('-publishdate')
        photoset = "notallphotos"
    photocategories = PhotoCategory.objects.all()
    descriptions = PhotoCategory.objects.filter(name=photocategory)
    tags = Tag.objects.all()
    toptags = Photo.tags.most_common()[:10]

    context = {'photocategories': photocategories, 'photos': photos, 'tags': tags, 'toptags': toptags, 'photoset':photoset, 'photocategory':photocategory, 'descriptions':descriptions}
    return render (request, 'photos/gallery.html', context)
 
class addPhoto(CreateView):
    model = Photo
    form_class = PhotoPostForm
    template_name = 'photos/add.html'
    success_url = reverse_lazy('gallery')

class PhotoPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoUpdateForm
    template_name = 'photos/update_photo_form.html'
    success_url = reverse_lazy('photo-update-success')

    def form_valid(self, form):
        form.instance.photographer = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.photographer:
            return True
        return False

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render (request, 'photos/photo.html', {'photo': photo})
 
def membergallery(request, pid):
    photos = Photo.objects.filter(photographer=pid)
    photocategories = PhotoCategory.objects.all()
    context = {'photocategories': photocategories, 'photos': photos}
    return render (request, 'photos/membergallery.html', context)

def photo_update(request):
    return render(request, 'photos/photo_update_success.html', {'title': 'Photo Updated'})

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['photocategories'] = PhotoCategory.objects.all()
        context['toptags'] = Photo.tags.most_common()[:10]
        return context

class TagIndexView(TagMixin, ListView):
    model = Photo
    template_name = 'photos/gallery.html'

    def get_context_data(self, **kwargs):
            context = super(TagMixin, self).get_context_data(**kwargs)
            context['tags'] = Tag.objects.all()
            context['photocategories'] = PhotoCategory.objects.all()
            context['toptags'] = Photo.tags.most_common()[:10]
            context['photos'] = Photo.objects.filter(Q(tags__slug=self.kwargs.get('tag_slug')),Q(approved=True))
            context['photoset'] = "allphotos"
            return context

def PhotoLikeView(request, pk):
    photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))
    photo.photolikes.add(request.user)
    return HttpResponseRedirect(reverse('viewphoto', args=[str(pk)]))

class PhotoDetailView(FormMixin, DetailView):
    model = Photo
    form_class = PhotoCreateCommentForm

    def get_context_data(self, *args, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Photo, id=self.kwargs['pk'])
        total_photolikes = stuff.total_photolikes()
        context["total_photolikes"] = total_photolikes
        context['form'] = PhotoCreateCommentForm(initial={'post': self.object, 'author': self.request.user})
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
        return super(PhotoDetailView, self).form_valid(form)