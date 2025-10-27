from django.views.generic import ListView, DetailView, View
from django.db.models import Prefetch
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from .models import Artwork
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
    - ``selected_condition``: filters by framing condition
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
            'category', 'selected_condition', 'main_photo'
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

        # Framing filtering
        framing = self.request.GET.get('selected_condition')
        if framing:
            queryset = queryset.filter(selected_condition__name=framing)

        # Price filtering
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(
                price__gte=min_price, price__lte=max_price
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_filtered_artworks = self.get_queryset()
        artworks_data = list(all_filtered_artworks.values(
            'id',
            'name',
            'description',
            'price',
            'is_available',
            'is_in_stock',
            'sku',
            'slug',
            'main_photo__image',
            'main_photo__alt_text'
        ))
        cleaned_artwork_data = []
        for item in artworks_data:
            cleaned_artwork_data.append({
                'id': item['id'],
                'name': item['name'],
                'description': item['description'],
                'price': float(item['price']),
                'is_available': item['is_available'],
                'is_in_stock': item['is_in_stock'],
                'sku': item['sku'],
                'slug': item['slug'],
                'image_public_id': item['main_photo__image'],
                'image_alt_text': item['main_photo__alt_text']
            })
        context['artworks_json_data'] = json.dumps(
            cleaned_artwork_data, cls=DjangoJSONEncoder
            )
        return context


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
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
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


# ---------------------------
# Artwork API view
# ---------------------------
class ArtworkAPIView(View):
    """
    API view to return a JSON list of artworks.

    If `GET`, returns a JSON response with all available artworks.

    **Response**
    A JSON array of artwork objects with fields:
    - ``id``
    - ``name``
    - ``description``
    - ``price``
    - ``is_available``
    - ``is_in_stock``
    - ``sku``
    - ``slug``

    **URL:**
    /api/artworks/
    """

    def get(self, request, *args, **kwargs):
        artworks_queryset = Artwork.objects.filter(is_available=True).values(
            'id',
            'name',
            'description',
            'price',
            'is_available',
            'is_in_stock',
            'sku',
            'slug',
            'main_photo__image',
            'main_photo__alt_text'
        )

        final_list = []
        for artwork_data in artworks_queryset:
            cleaned_artworks_item = {
                'id': artwork_data['id'],
                'name': artwork_data['name'],
                'description': artwork_data['description'],
                'price': float(artwork_data['price']),
                'is_available': artwork_data['is_available'],
                'is_in_stock': artwork_data['is_in_stock'],
                'sku': artwork_data['sku'],
                'slug': artwork_data['slug'],
                'image_public_id': artwork_data['main_photo__image'],
                'image_alt_text': artwork_data['main_photo__alt_text'],
            }
            final_list.append(cleaned_artworks_item)
        return JsonResponse(final_list, safe=False)
