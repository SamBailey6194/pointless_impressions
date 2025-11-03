from django.views.generic import ListView, DetailView, View
from django.db.models import Prefetch
from django.conf import settings
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.template.defaultfilters import truncatewords
from .models import Artwork, ArtworkCategory, ArtworkFramingCondition
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist


# ----------------------------
# Helper Functions
# ---------------------------
PLACEHOLDER_WORDS = 15


def get_placeholder_image():
    """Returns a placeholder image data."""
    try:
        return Photo.objects.get(asset_identifier='placeholder_image')
    except Photo.DoesNotExist:
        return None


def _serialize_artwork_data(artwork_queryset, placeholder_image):
    """
    Cleans and formats a queryset of Artwork objects into a list of
    dictionaries with comprehensive details (suitable for API use).

    Artwork objects must be prefetched with 'prefetched_conditions',
    'main_photo', 'category', and 'artist__user'.

    Args:
        artwork_queryset (QuerySet): A queryset of Artwork objects.
        placeholder_image (Photo or None): A Photo object for fallback.

    Returns:
        list: A list of dictionaries containing cleaned artwork data.
    """
    cleaned_data = []
    for artwork in artwork_queryset:
        # Image Data
        image_url = None
        image_public_id = None
        image_alt_text = artwork.name
        image_obj = artwork.main_photo or placeholder_image

        if image_obj:
            image_url_attr = getattr(image_obj, 'get_image_url', None)

            if callable(image_url_attr):
                image_url = image_url_attr()
            else:
                image_url = image_url_attr

            image_public_id = getattr(image_obj, 'asset_identifier', None)

            image_alt_text = getattr(
                image_obj,
                'alt_text_or_default',
                artwork.name
            )

        # Artist Data
        artist_data = None
        if hasattr(artwork, 'artist') and artwork.artist:
            user = artwork.artist.user
            artist_data = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': (
                    f"{user.first_name} {user.last_name}".strip()
                    ),
            }

        # Truncated Description
        full_desc = artwork.description
        truncated_desc = truncatewords(full_desc, PLACEHOLDER_WORDS)

        # Framing Condition Data
        conditions = [
            {'name': cond.condition_name, 'slug': cond.slug}
            for cond in getattr(artwork, 'prefetched_conditions', [])
        ]

        # Core Artwork Data
        item = {
            'id': artwork.id,
            'name': artwork.name,
            'artist': artist_data,
            'full_description': full_desc,
            'description': truncated_desc,
            'price': float(artwork.price),
            'category': artwork.category.name if artwork.category else None,
            'selected_conditions': conditions,
            'is_available': artwork.is_available,
            'is_in_stock': artwork.is_in_stock,
            'is_featured': artwork.is_featured,
            'sku': artwork.sku,
            'slug': artwork.slug,
            'image_url': image_url,
            'image_public_id': image_public_id,
            'image_alt_text': image_alt_text,
            'created_at': (
                artwork.created_at.isoformat() if
                getattr(artwork, 'created_at', None) else None
                ),
            'updated_at': (
                artwork.updated_at.isoformat() if
                getattr(artwork, 'updated_at', None) else None
            ),
            'quantity': artwork.quantity,
        }
        cleaned_data.append(item)
    return cleaned_data


# ---------------------------
# Artwork list view
# ---------------------------
class ArtworkListView(ListView):
    """
    Renders the public artwork list page with optional category,
    price, artist, and framing condition filters.

    If `GET`, returns a paginated list of available artworks filtered by query
    parameters:
    - ``category``: filters by artwork category
    - ``selected_condition``: filters by framing condition
    - ``min_price`` / ``max_price``: filters artworks by price range
    - ``artist``: filters by artist username

    **Context**
    ``artworks``
        A queryset of available Artwork objects, filtered and paginated.
    ``production``
        Boolean indicating if the site is in production mode.
    ``placeholder_image``
        A Photo object used as a placeholder for artworks without images.
    ``artwork_categories``
        A queryset of all ArtworkCategory objects for filtering.
    ``framing_conditions``
        A queryset of all ArtworkFramingCondition objects for filtering.
    ``all_artists``
        A queryset of all active Artist objects for filtering.
    ``artworks_json_data``
        A JSON string containing artwork data for use in frontend scripts.

    **Template:**
    :template:`artwork/artwork.html`
    """

    model = Artwork
    template_name = 'artwork/artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 12

    def get_queryset(self):
        queryset = Artwork.objects.filter(is_available=True).select_related(
            'category', 'main_photo', 'artist__user'
        ).prefetch_related(
            'photos',
            Prefetch(
                'selected_conditions',
                queryset=ArtworkFramingCondition.objects.only(
                    'condition_name', 'id', 'slug'
                    ), to_attr='prefetched_conditions'
            )
        )

        # Artist filtering
        artist_username = self.request.GET.get('artist')
        if artist_username:
            queryset = queryset.filter(artist__user__username=artist_username)

        # Category filtering
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Framing filtering
        framing_slug = self.request.GET.get('selected_conditions')
        if framing_slug:
            queryset = queryset.filter(
                selected_conditions__slug=framing_slug
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

        # Sorting
        sort_key = self.request.GET.get('sort', 'price')
        direction = self.request.GET.get('direction', 'asc')
        sort_map = {
            'price': 'price',
            'name': 'name',
            'artist': 'artist__user__username',
        }
        order_field = sort_map.get(sort_key, 'price')
        if direction == 'desc':
            order_field = '-' + order_field
        queryset = queryset.order_by(order_field)

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

        raw_artwork_data = _serialize_artwork_data(
            artworks_on_page, placeholder
            )

        cleaned_artwork_data = []
        for artwork in raw_artwork_data:
            cleaned_artwork_data.append({
                'id': artwork['id'],
                'name': artwork['name'],
                'description': artwork['description'],
                'price': float(artwork['price']),
                'category': artwork['category'],
                'selected_conditions': [
                    cond['name'] for cond in artwork['selected_conditions']
                ],
                'is_available': artwork['is_available'],
                'is_in_stock': artwork['is_in_stock'],
                'is_featured': artwork['is_featured'],
                'sku': artwork['sku'],
                'slug': artwork['slug'],
                'image_public_id': artwork['image_public_id'],
                'image_alt_text': artwork['image_alt_text'],
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
            'category', 'main_photo', 'artist__user'
        ).prefetch_related(
            'photos',
            Prefetch(
                'selected_conditions',
                queryset=ArtworkFramingCondition.objects.only(
                    'condition_name', 'id', 'slug'
                    ), to_attr='prefetched_conditions'
            )
        ).order_by('id')

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
    - ``id``
    - ``name``
    - ``artist``
    - ``description``
    - ``price``
    - ``category``
    - ``selected_conditions``
    - ``image_url``
    - ``image_public_id``
    - ``image_alt_text``
    - ``is_available``
    - ``is_in_stock``
    - ``sku``
    - ``slug``
    - ``created_at``
    - ``updated_at``

    **URL:**
    /api/artworks/
    """

    def get(self, request, *args, **kwargs):
        artworks_queryset = Artwork.objects.filter(
            is_available=True
            ).select_related(
            'main_photo', 'category', 'artist__user'
            ).prefetch_related(
            Prefetch(
                'selected_conditions',
                queryset=ArtworkFramingCondition.objects.only(
                    'condition_name', 'id', 'slug'
                    ), to_attr='prefetched_conditions'
                )
        ).order_by('id')

        placeholder = get_placeholder_image()

        final_list = _serialize_artwork_data(
            artworks_queryset, placeholder
            )

        cleaned_api_data = []
        for artwork in final_list:
            cleaned_api_data.append({
                'id': artwork['id'],
                'name': artwork['name'],
                'artist': artwork['artist'],
                'description': artwork['description'],
                'price': artwork['price'],
                'category': artwork['category'],
                'selected_conditions': artwork['selected_conditions'],
                'is_available': artwork['is_available'],
                'is_in_stock': artwork['is_in_stock'],
                'sku': artwork['sku'],
                'slug': artwork['slug'],
                'image_url': artwork['image_url'],
                'image_public_id': artwork['image_public_id'],
                'image_alt_text': artwork['image_alt_text'],
                'created_at': artwork['created_at'],
                'updated_at': artwork['updated_at'],
                'full_description': artwork['full_description'],
            })

        return JsonResponse(cleaned_api_data, safe=False)
