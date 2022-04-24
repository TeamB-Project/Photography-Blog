from django.shortcuts import render, redirect
from .models import Photo, PhotoCategory
from django.db.models import Q

def gallery(request):
    photocategory = request.GET.get('photocategory')
    if photocategory == None:
       photos = Photo.objects.filter(approved=True)
    else:
        photos = Photo.objects.filter(Q(photocategory__name=photocategory),Q(approved=True))
 
    photocategories = PhotoCategory.objects.all()
    context = {'photocategories': photocategories, 'photos': photos}
    return render (request, 'photos/gallery.html', context)

def addPhoto(request):
    photocategories = PhotoCategory.objects.all()  
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        if data['photocategory'] != 'none':
            photocategory = PhotoCategory.objects.get(id=data['photocategory'])
        else:
            photocategory = None
        photo = Photo.objects.create(
            photocategory=photocategory,
            description=data['description'],
            image=image,
            location=data['location'],
        )
        return redirect('gallery')
    context = {'photocategories': photocategories}
    return render (request, 'photos/add.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render (request, 'photos/photo.html', {'photo': photo})

def membergallery(request, pid):
    photos = Photo.objects.filter(photographer=pid)
    photocategories = PhotoCategory.objects.all()
    context = {'photocategories': photocategories, 'photos': photos}
    return render (request, 'photos/membergallery.html', context)