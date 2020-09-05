from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .models import Album, Artist, Contact, Booking

def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    template = loader.get_template('store/index.html')
    context = {'albums': albums}
    return HttpResponse(template.render(context,request=request))
    
def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 3)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
        'paginate':True
    }
    return render(request, 'store/listing.html', context)
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

