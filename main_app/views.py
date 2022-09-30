from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Artist

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        print(name)
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["artists"] = Artist.objects.filter(name__icontains=name)
        else:
            context["artists"] = Artist.objects.all()
        return context
