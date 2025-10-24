from django.shortcuts import render
from django.views.generic import ListView
from .models import Artwork


# Create your views here.
class ArtworkListView(ListView):
    model = Artwork
    template_name = 'artwork.html'  # points to your artwork.html template
    context_object_name = 'artworks'  # the name your template expects

    def get_queryset(self):
        """
        Return all artworks, optionally filter or sort later.
        """
        return Artwork.objects.all().order_by('id')
