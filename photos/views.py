from django.shortcuts import render, redirect
from .models import Photo, PhotoCategory
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import (PhotoPostForm, PhotoUpdateForm) #forms.py
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView
)
from django.urls import reverse_lazy
from taggit.models import Tag

def gallery(request):
    photocategory = request.GET.get('photocategory')
    if photocategory == None:
       photos = Photo.objects.filter(approved=True)
    else:
        photos = Photo.objects.filter(Q(photocategory__name=photocategory),Q(approved=True))
    photocategories = PhotoCategory.objects.all()
    tags = Tag.objects.all()

    context = {'photocategories': photocategories, 'photos': photos, 'tags': tags}
    return render (request, 'photos/gallery.html', context)
 
class addPhoto(CreateView):
    model = Photo
    form_class = PhotoPostForm
    template_name = 'photos/add.html'
    success_url = reverse_lazy('gallery')

class PhotoPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoUpdateForm
    template_name = 'photos/add.html'
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
    return render(request, 'photos/photo_update_success.html', {'title': 'Photo Updated'}) #Updated articles

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['photocategories'] = PhotoCategory.objects.all()
        return context

class TagIndexView(TagMixin, ListView):
    model = Photo
    template_name = 'photos/gallery.html'
    context_object_name = 'photos'

    def get_queryset(self):
        return Photo.objects.filter(tags__slug=self.kwargs.get('tag_slug'))