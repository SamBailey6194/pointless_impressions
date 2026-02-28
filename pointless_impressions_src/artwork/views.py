from django.views.generic import ListView, DetailView, View
from django.db.models import Prefetch
from django.conf import settings
import re
import json
from django.http import JsonResponse
from django.template.defaultfilters import truncatewords
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import (
    Artwork, ArtworkCategory, ArtworkFramingCondition
)
from .forms import AddToCartForm
from pointless_impressions_src.profiles.models import Artist
from pointless_impressions_src.cart.models import Cart
from pointless_impressions_src.photo.models import Photo


# ----------------------------
# Helper Functions
# ---------------------------
PLACEHOLDER_WORDS = 15


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

        # Use artwork's main_photo, NOT placeholder as fallback
        image_obj = artwork.main_photo

        if image_obj:

            try:
                image_alt_text = image_obj.alt_text_or_default
            except AttributeError:
                image_alt_text = artwork.name

            image_public_id = getattr(image_obj, 'asset_identifier', None)

            if not image_public_id and hasattr(
                image_obj, 'image'
            ) and image_obj.image:
                try:
                    raw_path = str(image_obj.image)
                    # Regex: Remove 'image/upload/' and version prefixes like
                    # 'v1/' or 'v12345/'
                    image_public_id = re.sub(
                        r'^(image/upload/)?(v\d+/)?', '', raw_path
                        )
                except (AttributeError, ValueError):
                    pass

            # Get image URL - for local dev with ImageField or Cloudinary
            image_url_attr = getattr(image_obj, 'get_image_url', None)

            if callable(image_url_attr):
                url_result = image_url_attr()
                # Only set if not empty string
                if url_result and url_result.strip():
                    image_url = url_result

            # Fallback: Try to get URL from image field directly
            if not image_url and hasattr(image_obj, 'image'):
                try:
                    img_field = getattr(image_obj, 'image', None)
                    if hasattr(img_field, 'url'):
                        try:
                            image_url = img_field.build_url(
                                width=2000, height=2000, crop='limit'
                            )
                        except Exception:
                            image_url = img_field.url
                    else:
                        image_url = str(img_field)
                except (AttributeError, ValueError):
                    pass
            else:
                # Fallback to placeholder if no main photo
                placeholder_image_obj = placeholder_image
                if placeholder_image_obj:
                    image_public_id = getattr(
                        placeholder_image_obj, 'asset_identifier', None
                        )

                    # Clean placeholder path if ID is missing
                    if not image_public_id and hasattr(
                        placeholder_image_obj, 'image'
                    ):
                        raw_path = str(placeholder_image_obj.image)
                        image_public_id = re.sub(
                            r'^(image/upload/)?(v\d+/)?', '', raw_path
                            )

                    image_url_attr = getattr(
                        placeholder_image_obj, 'get_image_url', None
                        )
                    if callable(image_url_attr):
                        image_url = image_url_attr()

            # Artist Data
            artist_data = None
            if hasattr(artwork, 'artist') and artwork.artist:
                user_profile = getattr(artwork.artist, 'user_profile', None)
                if user_profile:
                    user = user_profile.user
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
                {
                    'id': cond.id,
                    'name': cond.condition_name,
                    'friendly_name': cond.condition_friendly_name,
                    'slug': cond.slug
                }
                for cond in getattr(artwork, 'prefetched_conditions', [])
            ]

            # Core Artwork Data
            item = {
                'id': artwork.id,
                'name': artwork.name,
                'artist': artist_data,
                'full_description': full_desc,
                'description': truncated_desc,
                'price': round(float(artwork.price), 2),
                'category': (
                    artwork.category.name if artwork.category else None
                    ),
                'selected_conditions': conditions,
                'is_available': artwork.is_available,
                'is_in_stock': artwork.is_in_stock,
                'is_featured': artwork.is_featured,
                'sku': artwork.sku,
                'slug': artwork.slug,
                'image_url': image_url,
                'image_public_id': image_public_id,
                'image_alt_text': image_alt_text,
                'created_at': artwork.created_at.isoformat() if getattr(
                    artwork, 'created_at', None) else None,
                'updated_at': artwork.updated_at.isoformat() if getattr(
                    artwork, 'updated_at', None) else None,
                'quantity': artwork.quantity,
            }
            cleaned_data.append(item)
    return cleaned_data


def get_placeholder_image_from_context(request):
    """
    Helper function to get placeholder image from request context.
    Falls back to database query if context is not available.

    Args:
        request: Django request object
        (may have context from context processor)

    Returns:
        Photo object or None
    """
    # This helper is primarily for API views that don't have template context
    try:
        return Photo.objects.get(asset_identifier='placeholder_image')
    except Photo.DoesNotExist:
        return None


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
    ``artwork_categories``
        A queryset of all ArtworkCategory objects for filtering.
    ``framing_conditions``
        A queryset of all ArtworkFramingCondition objects for filtering.
    ``all_artists``
        A queryset of all active Artist objects for filtering.
    ``artworks_json_data``
        A JSON string containing artwork data for use in frontend scripts.

    **Template:**
    :template:`artwork/artwork_list.html`
    """

    model = Artwork
    template_name = 'artwork/artwork_list.html'
    context_object_name = 'artworks'
    paginate_by = 12

    def get_queryset(self):
        queryset = Artwork.objects.all().select_related(
            'category', 'main_photo', 'artist__user_profile__user'
        ).prefetch_related(
            'photos',
            Prefetch(
                'selected_conditions',
                queryset=ArtworkFramingCondition.objects.only(
                    'condition_name', 'id', 'slug'
                    ), to_attr='prefetched_conditions'
            )
        )

        general_filter = self.request.GET.get('filter')
        available_only = self.request.GET.get('available_only')
        if general_filter == 'available' or available_only == 'on':
            queryset = queryset.filter(is_available=True)

        artist_username = self.request.GET.get('artist')
        if artist_username:
            queryset = queryset.filter(
                artist__user_profile__user__username=artist_username
                )

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        framing_slug = self.request.GET.get('selected_conditions')
        if framing_slug:
            queryset = queryset.filter(
                selected_conditions__slug=framing_slug
            )

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

        sort_key = self.request.GET.get('sort', 'price')
        direction = self.request.GET.get('direction', 'asc')
        sort_map = {
            'price': 'price',
            'name': 'name',
            'artist': 'artist__user_profile__user__username',
        }
        order_field = sort_map.get(sort_key, 'price')
        if direction == 'desc':
            order_field = '-' + order_field
        queryset = queryset.order_by(order_field)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        artworks_on_page = context['artworks']
        for artwork in artworks_on_page:
            if artwork.is_available:
                artwork.add_to_cart_form = AddToCartForm(artwork_id=artwork.id)
            else:
                artwork.add_to_cart_form = None

        placeholder = context.get('placeholder_image')

        raw_artwork_data = _serialize_artwork_data(
            artworks_on_page, placeholder
        )
        context['artworks_json_data'] = json.dumps(raw_artwork_data)

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

    Add to Cart Form:
        An instance of the AddToCartForm for adding the artwork to cart.
        Uses AJAX submission for the frontend to make UX seamless.

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
            'category', 'main_photo', 'artist__user_profile__user'
        ).prefetch_related(
            'photos',
            Prefetch(
                'selected_conditions',
                queryset=ArtworkFramingCondition.objects.only(
                    'condition_name', 'id', 'slug', 'condition_friendly_name'
                    ), to_attr='prefetched_conditions'
            )
        ).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.get_object()

        placeholder = context.get('placeholder_image')

        serialized_data_list = _serialize_artwork_data(
            [artwork], placeholder
        )

        artwork_data = serialized_data_list[0]
        context['artwork_data'] = artwork_data

        all_photos = artwork.photos.all()
        context['carousel_photos'] = all_photos

        context['prefetched_conditions'] = artwork.prefetched_conditions

        framing_options = []
        for condition in artwork.prefetched_conditions:
            framing_options.append({
                'id': condition.id,
                'name': (
                    condition.condition_friendly_name or
                    condition.condition_name
                ),
                'slug': condition.slug
            })
        context['framing_options_json'] = json.dumps(framing_options)

        if artwork.artist:
            similar_artists = Artwork.objects.filter(
                artist=artwork.artist
            ).exclude(
                pk=artwork.pk
            ).select_related(
                'main_photo', 'artist__user_profile__user'
            )[:10]
            context['similar_artists'] = similar_artists

        if artwork.category:
            similar_artworks = Artwork.objects.filter(
                category=artwork.category
            ).exclude(
                pk=artwork.pk
            ).select_related(
                'main_photo', 'artist__user_profile__user'
            )[:10]
            context['similar_artworks'] = similar_artworks

        context['add_to_cart_form'] = AddToCartForm(artwork_id=artwork.id)

        # Pass the stock quantity to the context
        context['stock'] = artwork.quantity

        # Set the form action to the current page URL
        context['form_action'] = self.request.path

        # Include session ID in the context for the frontend
        context['sessionid'] = self.request.session.session_key

        # Ensuring session ID exists
        session_id = self.request.session.session_key
        if not session_id:
            self.request.session.create()
            session_id = self.request.session.session_key

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the Add to Cart functionality.
        Validates the AddToCartForm and updates the cart in the database.
        """
        artwork = self.get_object()

        form = AddToCartForm(request.POST, artwork_id=artwork.id)
        if form.is_valid():
            framing_option = form.cleaned_data.get('framing_option')

            # Retrieve or create the cart for the current session
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key

            cart, created = Cart.get_or_create_from_sessionid(session_id)

            quantity = form.cleaned_data.get('quantity')
            notes = form.cleaned_data.get('notes', '')

            cart.add_or_update_item(
                artwork=artwork,
                quantity=quantity,
                framing_condition=framing_option,
                notes=notes
            )

            total_quantity = cart.get_total_quantity()

            return JsonResponse(
                {
                    'success': True,
                    'message': ' Artwork added to cart.',
                    'cart_count': total_quantity,
                    'total_quantity': total_quantity
                    }
                )

        return JsonResponse(
            {'success': False, 'errors': form.errors}, status=400
        )


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
            'main_photo', 'category', 'artist__user_profile__user'
            ).prefetch_related(
            Prefetch(
                'selected_conditions',
                queryset=ArtworkFramingCondition.objects.only(
                    'condition_name', 'id', 'slug'
                    ), to_attr='prefetched_conditions'
                )
        ).order_by('id')

        placeholder = get_placeholder_image_from_context(request)

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


# ----------------------------
# Development/Test-Only Views
# ----------------------------

@require_http_methods(["GET"])
def setup_test_data(request):
    """
    DEVELOPMENT ONLY - Test data creation endpoint.

    API endpoint to create test data for Cypress E2E tests.
    ONLY available when using test.py settings (SQLite test database).

    This endpoint:
    - Is protected by a test-mode database check
    - Creates sample artworks (Sunset, Starry Night)
    - Creates required artist and category records

    Args:
        request: HTTP request object

    Returns:
        JSON response with created artworks or error message

    Raises:
        PermissionDenied: If not running with test settings
    """
    try:
        db_name = settings.DATABASES.get('default', {}).get('NAME', '')
        is_test_mode = 'test' in db_name.lower()

        if not is_test_mode:
            error_msg = (
                'This endpoint only works with test.py settings '
                '(test database)'
            )
            return JsonResponse({
                'error': error_msg
            }, status=403)

        User = get_user_model()

        if Artwork.objects.filter(name='Sunset').exists():
            return JsonResponse({
                'message': 'Test data already exists',
                'artworks_created': False
            })

        default_artist_user = User.objects.create(
            username='test_artist',
            email='test_artist@example.com',
            phone='1234567890'
        )

        default_artist_profile = Artist.objects.create(
            user_profile=default_artist_user.user_profile,
            bio="Test artist bio",
            portfolio_url="https://testartist.com"
        )

        default_category = ArtworkCategory.objects.create(
            name="Pointillism",
            friendly_name="Pointillism Art",
            description="Beautiful pointillism artworks."
        )

        default_framing_condition = ArtworkFramingCondition.objects.create(
            condition_name="unframed",
            condition_description="Artwork is unframed."
        )

        test_artworks = [
            {
                'name': 'Sunset',
                'description': 'A beautiful sunset over the mountains.',
                'price': 199.99,
                'sku': 'SUNSET001',
                'is_available': True,
                'is_in_stock': True,
                'quantity': 5,
            },
            {
                'name': 'Starry Night',
                'description': 'A night sky full of stars.',
                'price': 249.99,
                'sku': 'STARRY001',
                'is_available': False,
                'is_in_stock': False,
                'quantity': 0,
            }
        ]

        created_artworks = []
        for artwork_data in test_artworks:
            art = Artwork.objects.create(
                name=artwork_data['name'],
                artist=default_artist_profile,
                category=default_category,
                description=artwork_data['description'],
                price=artwork_data['price'],
                sku=artwork_data['sku'],
                is_available=artwork_data['is_available'],
                is_in_stock=artwork_data['is_in_stock'],
                is_featured=False,
                quantity=artwork_data['quantity'],
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            art.selected_conditions.add(default_framing_condition)
            created_artworks.append(art.name)

        return JsonResponse({
            'message': 'Test data created successfully',
            'artworks_created': created_artworks
        }, status=201)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
