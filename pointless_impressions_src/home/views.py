from django.views.generic import TemplateView
from pointless_impressions_src.artwork.models import Artwork


# Create your views here.
class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_slug'] = 'home'
        # Section classes for the three-section template
        context['section_1_class'] = 'py-20 section-blue w-full'
        context['section_2_class'] = 'py-16 section-alt w-full'
        context['section_3_class'] = 'py-16 section-alt w-full'

        # Add featured artworks to context
        context['featured_artworks'] = Artwork.objects.filter(is_featured=True)

        return context
