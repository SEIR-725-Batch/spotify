from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from .models import Artist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# after our other imports 
from django.views.generic import DetailView

# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"

class ArtistList(TemplateView):
    template_name = "artist_list.html"
#     In here, I want to check if there has been a query made
# I know the queries will have a key of name
# const context = {
#     artists: //finding ArtistList,
#     stuff_at_top: "This is a string"
# }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mySearchName = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if mySearchName != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["artists"] = Artist.objects.filter(name__icontains=mySearchName)
            context["stuff_at_top"] = f"Searching through Artists list for {mySearchName}"
        else:
            context["artists"] = Artist.objects.all()
            context["stuff_at_top"] = "Trending Artists"
        return context

class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio']
    template_name = "artist_create.html"
    success_url = "/artists/"

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artist_detail.html"

class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_update.html"
    success_url = "/artists/"

    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})

class ArtistDelete(DeleteView):
    model = Artist
    template_name = "artist_delete_confirmation.html"
    success_url = "/artists/"