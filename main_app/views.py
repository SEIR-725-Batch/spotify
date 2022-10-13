# at top of file
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.views.generic.base import TemplateView
from .models import Artist, Song, Playlist, Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# after our other imports 
from django.views.generic import DetailView
# at top of file with other imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework import generics
from .serializers import ArtistSerializer, SongSerializers
from .models import Artist

# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

    # adding playlist context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = Playlist.objects.all()
        return context

class About(TemplateView):
    template_name = "about.html"

class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


@method_decorator(login_required, name='dispatch')
class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio']
    template_name = "artist_create.html"

    # This is our new method that will add the user into our submitted form
    def form_valid(self, form):
        # form.instance = {
            # name: Baby Shark 2,
            # img: my image url,
            # Bio: Some string
        # }
        form.instance.user = self.request.user
        # form.instance = {
            # name: Another Test,
            # img: a.com,
            # Bio: Proving a point,
            # user: self.request.user
        # }
        # form.instance.verified_artist = False
        return super(ArtistCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

@method_decorator(login_required, name='dispatch')
class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_update.html"
    success_url = "/artists/"

    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class ArtistDelete(DeleteView):
    model = Artist
    template_name = "artist_delete_confirmation.html"
    success_url = "/artists/"

@method_decorator(login_required, name='dispatch')
class SongCreate(View):

    def post(self, request, pk):
        formTitle = request.POST.get("title")
        minutes = request.POST.get("minutes")
        seconds = request.POST.get("seconds")
        formLength = 60 * int(minutes) + int(seconds)
        theArtist = Artist.objects.get(pk=pk)
        Song.objects.create(title=formTitle, length=formLength, artist=theArtist)
        return redirect('artist_detail', pk=pk)

class PlaylistSongAssoc(View):

    def get(self, request, pk, song_pk):
        # get the query parameter from the 
        assoc = request.GET.get("assoc")

        if assoc == "remove":
            # get the playlist by the pk, remove the song (row) with the song_pk
            Playlist.objects.get(pk=pk).songs.remove(song_pk)
        
        if assoc == "add":

            # get the playlist by the pk, add the song (row) with the song_pk
            Playlist.objects.get(pk=pk).songs.add(song_pk)
        
        return redirect('home')

class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("artist_list")
        else:
            return redirect("signup")

class ProfileCreate(CreateView):
    model = Profile
    fields = ['user', 'favorite_color', 'state_abbrev']
    template_name = "profile_create.html"
    success_url= "/"

def artist_list(request):
    artists = Artist.objects.all().values('name', 'img', 'bio', 'verified_artist', 'user') # only grab some attributes from our database, else we can't serialize it.
    artists_list = list(artists) # convert our artists to a list instead of QuerySet
    return JsonResponse(artists_list, safe=False) # safe=False is needed if the first parameter is not a dictionary.

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializers

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializers
