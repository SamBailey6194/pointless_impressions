from django.views.generic import ListView, DetailView
from .models import Artwork
from django.db.models import Prefetch
from pointless_impressions_src.photo.models import Photo


# ---------------------------
# Artwork list view
# ---------------------------
class ArtworkListView(ListView):
    """
    Renders the public artwork list page with optional search, category,
    and price filters.

    If `GET`, returns a paginated list of available artworks filtered by query
    parameters:
    - ``search``: searches by artwork name
    - ``category``: filters by artwork category
    - ``min_price`` / ``max_price``: filters artworks by price range

    **Context**
    ``artworks``
        A queryset of available Artwork objects, filtered and paginated.
    ``page_obj``
        Pagination object for navigating pages.

    **Template:**
    :template:`artwork/artwork.html`
    """

    model = Artwork
    template_name = 'artwork/artwork_list.html'
    context_object_name = 'artwork'
    paginate_by = 10

    def get_queryset(self):
        queryset = Artwork.objects.filter(is_available=True).select_related(
            'category', 'selected_condition'
        ).prefetch_related(
            Prefetch(
                'photo_set', queryset=Photo.objects.all(), to_attr='photos'
                )
        ).order_by('id')

        # Search functionality
        search_term = self.request.GET.get('search')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        # Category filtering
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)

        # Price filtering
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(
                price__gte=min_price, price__lte=max_price
                )

        return queryset


# ---------------------------
# Artwork detail view
# ---------------------------
class ArtworkDetailView(DetailView):
    """
    Renders the public artwork detail page.

    If `GET`, returns a single artwork by ID, including stock and availability
    status.

    **Context**
    ``artwork``
        An instance of the Artwork model.

    **Template:**
    :template:`artwork/artwork_detail.html`
    """

    model = Artwork
    template_name = 'artwork/artwork_detail.html'
    context_object_name = 'artwork'

    def get_queryset(self):
        return Artwork.objects.select_related(
            'category', 'selected_condition'
        ).prefetch_related(
            Prefetch(
                'photo_set', queryset=Photo.objects.all(), to_attr='photos'
                )
        )
