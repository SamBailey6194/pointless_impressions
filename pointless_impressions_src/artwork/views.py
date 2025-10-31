from django.views.generic import ListView, DetailView, View
from django.conf import settings
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from .models import Artwork, ArtworkCategory, ArtworkFramingCondition
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist


# ----------------------------
# Helper Functions
# ---------------------------
def get_placeholder_image():
    """Returns a placeholder image data."""
    try:
        return Photo.objects.get(asset_identifier='noimage_placeholder')
    except Photo.DoesNotExist:
        return None


# ---------------------------
# Artwork list view
# ---------------------------
class ArtworkListView(ListView):
    """
    Renders the public artwork list page with optional search, category,
    and price filters.

    If `GET`, returns a paginated list of available artworks filtered by query
    parameters:
    - ``search``: searches artwork name, category, and framing condition and
        ensures distinct results
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
    context_object_name = 'artworks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Artwork.objects.filter(is_available=True).select_related(
            'category', 'selected_condition', 'main_photo'
        ).prefetch_related('photos').order_by('id')

        # Artist filtering
        artist_username = self.request.GET.get('artist')
        if artist_username:
            queryset = queryset.filter(artist__user__username=artist_username)

        # Category filtering
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Framing filtering
        framing_slug = self.request.GET.get('selected_condition')
        if framing_slug:
            queryset = queryset.filter(
                selected_condition__slug=framing_slug
            )

        # Price filtering
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(
                price__gte=min_price, price__lte=max_price
                )
        elif min_price:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['production'] = not settings.DEBUG
        context['placeholder_image'] = get_placeholder_image()
        context['artwork_categories'] = (
            ArtworkCategory.objects.all()
            )
        context['framing_conditions'] = (
            ArtworkFramingCondition.objects.all()
            )
        context['all_artists'] = Artist.objects.select_related(
            'user').filter(user__is_active=True).order_by('user__username')
        # Prepare JSON data for artworks on the current page
        artworks_on_page = context['artworks']
        placeholder = context['placeholder_image']
        cleaned_artwork_data = []
        for artwork in artworks_on_page:
            # Safely get the image path (which is a string, suitable for JSON)
            image_url = None
            image_alt_text = artwork.name
            image_obj = artwork.main_photo or placeholder

            if image_obj:
                image_url = image_obj.get_image_url
                image_alt_text = image_obj.alt_text_or_default
            cleaned_artwork_data.append({
                'id': artwork.id,
                'name': artwork.name,
                'description': artwork.description,
                'price': float(artwork.price),
                'is_available': artwork.is_available,
                'is_in_stock': artwork.is_in_stock,
                'sku': artwork.sku,
                'slug': artwork.slug,
                'image_public_id': image_url,
                'image_alt_text': image_alt_text
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
        ).prefetch_related('photos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['production'] = not settings.DEBUG
        context['placeholder_image'] = get_placeholder_image()
        artwork = self.get_object()
        photos = artwork.photos.all()
        if artwork.main_photo:
            photos = photos.exclude(pk=artwork.main_photo.pk)
        context['photos'] = photos
        return context


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
        artworks_queryset = Artwork.objects.filter(
            is_available=True
            ).select_related(
            'main_photo'
        )

        placeholder = get_placeholder_image()

        final_list = []
        for artwork_data in artworks_queryset:
            image_url = None
            image_alt_text = artwork_data.name
            image_obj = artwork_data.main_photo or placeholder

            if image_obj:
                image_url = image_obj.get_image_url
                image_alt_text = image_obj.alt_text_or_default

            cleaned_artworks_item = {
                'id': artwork_data['id'],
                'name': artwork_data['name'],
                'artist': artwork_data['artist'],
                'description': artwork_data['description'],
                'price': float(artwork_data['price']),
                'is_available': artwork_data['is_available'],
                'is_in_stock': artwork_data['is_in_stock'],
                'sku': artwork_data['sku'],
                'slug': artwork_data['slug'],
                'image_url': image_url,
                'image_alt_text': image_alt_text,
            }
            final_list.append(cleaned_artworks_item)
        return JsonResponse(final_list, safe=False)
