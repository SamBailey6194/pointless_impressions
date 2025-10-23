from django.views.generic import TemplateView


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
        return context
