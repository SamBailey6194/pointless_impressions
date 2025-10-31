from django.views.generic import ListView, View
from django.db.models import Q
from django.http import JsonResponse
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkCategory, ArtworkFramingCondition
    )


# Create your views here.
class SearchView(ListView):
    """
    Renders the global search results page, compiling results from multiple
    models (currently Artwork and related fields).

    This view retrieves relevant objects based on the user's query and applies
    pagination.

    **Context**
    - ``results``: A paginated list of objects matching the search query.
    - ``page_obj``: Pagination object for navigating pages.
    - ``search_query``: The original search term entered by the user.

    **URL Parameters**
    - ``q``: The primary query parameter (e.g., /search/?q=sunset).

    **Template:**
    :template:`search/results.html`
    """
    model = Artwork
    template_name = 'search/results.html'
    context_object_name = 'results'
    paginate_by = 10 

    def get_queryset(self):
        query = self.request.GET.get('q')

        if not query:
            return Artwork.objects.none()

        artwork_search_q = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(selected_condition__condition_name__icontains=query)
        )

        artwork_results = Artwork.objects.filter(
            is_available=True
        ).filter(artwork_search_q).distinct().select_related(
            'category', 'selected_condition'
        ).prefetch_related('photos')

        return artwork_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class SearchAutocompleteView(View):
    """
    Provides JSON responses for search autocomplete functionality.

    This view processes AJAX requests containing a search term and returns
    a list of matching Artwork names to assist users in quickly finding items.

    **URL Parameters**
    - ``term``: The search term input by the user
        (e.g., /search/autocomplete/?term=sun).

    **Response Format**
    - JSON array of strings representing matching Artwork names.

    **Example Response**
    .. code-block:: json

        [
            "Sunset Overdrive",
            "Sunny Meadows",
            "Sunrise Bliss"
        ]
    """
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')

        if len(term) < 2:
            return JsonResponse([], safe=False)

        artwork_matches = Artwork.objects.filter(
            is_available=True,
            name__icontains=term
        ).values_list('name', flat=True)

        category_matches = ArtworkCategory.objects.filter(
            name__icontains=term
        ).values_list('name', flat=True)

        condition_matches = ArtworkFramingCondition.objects.filter(
            condition_name__icontains=term
        ).values_list('condition_name', flat=True)

        combined_results = set(artwork_matches)
        combined_results.update(category_matches)
        combined_results.update(condition_matches)

        final_list = sorted(list(combined_results))[:10]

        return JsonResponse(final_list, safe=False)
