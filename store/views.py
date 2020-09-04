from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Album, Artist, Contact, Booking

def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    template = loader.get_template('store/index.html')
    context = {'albums': albums}
    return HttpResponse(template.render(context,request=request))
    

def listing(request):
    albums = Album.objects.filter(available=True)
    context = {
        'albums': albums
    }
    template = loader.get_template('store/listing.html')
    return HttpResponse(template.render(context,request=request))
...
def detail(request, album_id):

    album = Album.objects.get(pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    template = loader.get_template('store/detail.html')
    return HttpResponse(template.render(context,request=request))
    ...
def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'albums': albums,
        'title': title
    }
    return render(request, 'store/search.html', context)

