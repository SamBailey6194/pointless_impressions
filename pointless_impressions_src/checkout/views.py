from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib import messages
from pointless_impressions_src.artwork.models import (
    Artwork, ArtworkFramingCondition
    )
from .models import Cart, CartItem
from .forms import (
    AddToCartForm,
    UpdateCartQuantityForm,
    RemoveFromCartForm,
    SyncCartForm,
)


# Write your views here.
class CheckoutView(TemplateView):
    """
    GET /checkout/
    Display main checkout page with cart review and payment form

    Context Data:
    - cart_items: List of items in cart with artwork details
    - total_price: Sum of all item totals (float)
    - total_quantity: Total number of items in cart (int)

    Features:
    - Retrieves cart from Cart/CartItem models using UUID or user
    - Calculates line totals and grand total
    - Removes items if artwork no longer exists
    - Displays cart summary and checkout form

    Response: Renders checkout.html template with cart context
    """
    template_name = 'checkout/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get cart by UUID (from GET param or cookie) or user
        cart_uuid = (
            self.request.GET.get('cart_uuid') or
            self.request.COOKIES.get('cart_uuid')
            )
        cart, _ = CartAPIView().get_or_create_cart(self.request, cart_uuid)

        cart_items = []
        total_price = 0
        total_quantity = 0

        if cart:
            for item in cart.items.select_related('artwork').all():
                artwork = item.artwork
                item_total = float(artwork.price) * item.quantity
                total_price += item_total
                total_quantity += item.quantity
                cart_items.append({
                    'artwork': artwork,
                    'quantity': item.quantity,
                    'price': float(artwork.price),
                    'total': item_total,
                    'framing_option': item.framing_condition,
                    'notes': item.notes,
                })

        context.update({
            'cart_items': cart_items,
            'total_price': total_price,
            'total_quantity': total_quantity,
        })

        return context


class CartAPIView(View):
    """
    Base class for cart API endpoints

    Methods:
    - get_or_create_cart(): Get/create cart from UUID or authenticated user
    - get_cart_count(): Get total quantity of items in cart

    All cart operations inherit from this class for consistent
    cart management using Cart/CartItem models.
    """
    def get_or_create_cart(self, request, cart_uuid=None):
        if request.user.is_authenticated:
            # Authenticated users get their cart
            cart, created = Cart.objects.get_or_create(
                user=request.user,
                defaults={'is_active': True}
            )
            return cart, created
        elif cart_uuid:
            # Anonymous users with UUID
            cart, created = Cart.get_or_create_from_uuid(cart_uuid)
            return cart, created if cart else (None, False)
        else:
            # Create new anonymous cart with new UUID
            cart = Cart.objects.create(is_active=True)
            return cart, True

    def get_cart_count(self, cart):
        """Get total quantity of items in cart"""
        if not cart:
            return 0
        return cart.get_total_items()


@method_decorator(require_http_methods(['POST']), name='dispatch')
class AddToCartView(CartAPIView):
    """
    POST /checkout/api/cart/add/
    Add item to cart and save to Cart/CartItem models

    Required POST data:
    - artwork_id: int
    - quantity: int (1-999)

    Optional POST data:
    - framing_condition_id: int (FK to ArtworkFramingCondition)
    - notes: str (max 500 chars)

    Query Parameters:
    - cart_uuid: UUID of existing cart (for anonymous users)

    Response: {
        success: bool,
        cart_uuid: str (UUID),
        cart_count: int,
        message: str
    }
    """

    def post(self, request):
        # Parse form data
        form = AddToCartForm(request.POST)

        if not form.is_valid():
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors,
                },
                status=400
            )

        artwork_id = form.cleaned_data['artwork_id']
        quantity = form.cleaned_data['quantity']
        framing_option = form.cleaned_data.get('framing_option')
        notes = form.cleaned_data.get('notes', '')

        # Get artwork
        try:
            artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Artwork not found'},
                status=404
            )

        # SECURITY: Validate quantity is safe (prevent 0 or negative)
        if quantity < 1:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Quantity must be at least 1',
                    'type': 'error',
                },
                status=400
            )

        # SECURITY: Validate artwork is in stock
        if not artwork.is_in_stock or not artwork.is_available:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'This artwork is no longer available',
                    'type': 'error',
                },
                status=400
            )

        # Get or create cart from UUID or user
        cart_uuid = request.GET.get('cart_uuid')
        cart, _ = self.get_or_create_cart(request, cart_uuid)

        if not cart:
            return JsonResponse(
                {'success': False, 'message': 'Failed to create cart'},
                status=400
            )

        # Get or create cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, artwork=artwork)
            new_quantity = cart_item.quantity + quantity
        except CartItem.DoesNotExist:
            new_quantity = quantity

        # SECURITY: Validate total quantity against stock
        if new_quantity > artwork.quantity:
            return JsonResponse(
                {
                    'success': False,
                    'message': f'Only {artwork.quantity} units available',
                    'type': 'error',
                },
                status=400
            )

        # Handle framing condition if provided
        framing_condition = None
        if framing_option:
            try:
                framing_condition = (
                    ArtworkFramingCondition.objects.get(
                        id=framing_option
                    )
                )
                # Validate framing option is in artwork's selected
                if not artwork.selected_conditions.filter(
                    id=framing_condition.id
                ).exists():
                    return JsonResponse(
                        {
                            'success': False,
                            'message': (
                                'Invalid framing option for this artwork'
                            ),
                            'type': 'error',
                        },
                        status=400
                    )
            except ArtworkFramingCondition.DoesNotExist:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'Framing condition not found',
                    },
                    status=404
                )

        # Create or update cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            artwork=artwork,
            defaults={
                'quantity': new_quantity,
                'framing_condition': framing_condition,
                'notes': notes,
            }
        )

        # Add Django message
        message_text = f'{artwork.name} added to cart'
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_uuid': str(cart.uuid),
                'cart_count': self.get_cart_count(cart),
            },
            status=200
        )


@method_decorator(require_http_methods(['POST']), name='dispatch')
class RemoveFromCartView(CartAPIView):
    """
    POST /checkout/api/cart/remove/
    Remove item from cart

    Required POST data:
    - artwork_id: int

    Query Parameters:
    - cart_uuid: UUID of cart (for anonymous users)

    Response: {success: bool, cart_count: int, message: str}
    """

    def post(self, request):
        form = RemoveFromCartForm(request.POST)

        if not form.is_valid():
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors,
                },
                status=400
            )

        artwork_id = form.cleaned_data['artwork_id']

        # Get or create cart from UUID or user
        cart_uuid = request.GET.get('cart_uuid')
        cart, _ = self.get_or_create_cart(cart_uuid)

        if not cart:
            return JsonResponse(
                {'success': False, 'message': 'Failed to access cart'},
                status=400
            )

        # Remove cart item
        try:
            cart_item = CartItem.objects.get(
                cart=cart,
                artwork_id=artwork_id
            )
            cart_item.delete()
        except CartItem.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Item not in cart'},
                status=404
            )

        # Add Django message
        message_text = 'Item removed from cart'
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_uuid': str(cart.uuid),
                'cart_count': self.get_cart_count(cart),
            },
            status=200
        )


@method_decorator(require_http_methods(['POST']), name='dispatch')
class UpdateCartQuantityView(CartAPIView):
    """
    POST /checkout/api/cart/update/
    Update quantity of item in cart

    Required POST data:
    - artwork_id: int
    - quantity: int (0-999, 0 to remove)

    Query Parameters:
    - cart_uuid: UUID of cart (for anonymous users)

    Response: {success: bool, cart_count: int, message: str}
    """

    def post(self, request):
        form = UpdateCartQuantityForm(request.POST)

        if not form.is_valid():
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors,
                },
                status=400
            )

        artwork_id = form.cleaned_data['artwork_id']
        quantity = form.cleaned_data['quantity']

        # Get or create cart from UUID or user
        cart_uuid = request.GET.get('cart_uuid')
        cart, _ = self.get_or_create_cart(request, cart_uuid)

        if not cart:
            return JsonResponse(
                {'success': False, 'message': 'Failed to access cart'},
                status=400
            )

        # Get cart item
        try:
            cart_item = CartItem.objects.get(
                cart=cart,
                artwork_id=artwork_id
            )
        except CartItem.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Item not in cart'},
                status=404
            )

        # Get artwork to validate against stock
        artwork = cart_item.artwork

        # SECURITY: Validate quantity is not negative
        if quantity < 0:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Quantity cannot be negative',
                    'type': 'error',
                },
                status=400
            )

        if quantity == 0:
            # Remove item if quantity is 0
            cart_item.delete()
            message_text = 'Item removed from cart'
        else:
            # SECURITY: Validate artwork is still available
            if not artwork.is_in_stock or not artwork.is_available:
                return JsonResponse(
                    {
                        'success': False,
                        'message': (
                            'This artwork is no longer available'
                        ),
                        'type': 'error',
                    },
                    status=400
                )

            # SECURITY: Validate quantity against stock
            if quantity > artwork.quantity:
                return JsonResponse(
                    {
                        'success': False,
                        'message': (
                            f'Only {artwork.quantity} units available'
                        ),
                        'type': 'error',
                    },
                    status=400
                )

            cart_item.quantity = quantity
            cart_item.save()
            message_text = 'Cart updated'

        # Add Django message
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_uuid': str(cart.uuid),
                'cart_count': self.get_cart_count(cart),
            },
            status=200
        )


@method_decorator(require_http_methods(['POST']), name='dispatch')
class SyncCartView(CartAPIView):
    """
    POST /checkout/api/cart/sync/
    Sync localStorage cart with backend models (Cart/CartItem)

    Required JSON body:
    {
      "cart": {
        "artwork_id": {
          "id": int,
          "name": str,
          "price": float,
          "quantity": int,
          "framing_option": int (optional),
          "notes": str (optional)
        }
      }
    }

    Query Parameters:
    - cart_uuid: UUID of cart (for anonymous users)

    Response: {success: bool, cart_uuid: str, cart_count: int, message: str}
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {'success': False, 'message': 'Invalid JSON'},
                status=400
            )

        form = SyncCartForm(data)

        if not form.is_valid():
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors,
                },
                status=400
            )

        cart_data = form.cleaned_data['cart']
        cart_uuid = request.GET.get('cart_uuid')
        cart, _ = self.get_or_create_cart(request, cart_uuid)
        if not cart:
            return JsonResponse(
                {'success': False, 'message': 'Failed to create cart'},
                status=400
                )

        # Remove all existing items for this cart (full sync)
        CartItem.objects.filter(cart=cart).delete()

        # Add all items from posted cart
        for artwork_id, item in cart_data.items():
            try:
                artwork = Artwork.objects.get(id=artwork_id)
            except Artwork.DoesNotExist:
                continue  # skip invalid
            quantity = item.get('quantity', 1)
            framing_option = item.get('framing_option')
            notes = item.get('notes', '')
            framing_condition = None
            if framing_option:
                try:
                    framing_condition = ArtworkFramingCondition.objects.get(
                        id=framing_option
                        )
                except ArtworkFramingCondition.DoesNotExist:
                    framing_condition = None
            CartItem.objects.create(
                cart=cart,
                artwork=artwork,
                quantity=quantity,
                framing_condition=framing_condition,
                notes=notes,
            )

        message_text = 'Cart synced'
        messages.success(request, message_text)
        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_uuid': str(cart.uuid),
                'cart_count': self.get_cart_count(cart),
            },
            status=200
        )


@method_decorator(csrf_exempt, name='dispatch')
class CartFetchView(CartAPIView):
    """
    GET /checkout/api/cart/fetch/?cart_uuid=...
    Returns cart data as JSON for frontend display
    Response: {
        cart_uuid: str,
        items: [
            {
                artwork_id: int,
                name: str,
                price: float,
                quantity: int,
                total: float,
                framing_option: str or null,
                notes: str
            }, ...
        ],
        subtotal: float,
        total_items: int
    }
    """
    def get(self, request):
        cart_uuid = request.GET.get('cart_uuid')
        cart, _ = self.get_or_create_cart(request, cart_uuid)
        items = []
        subtotal = 0
        total_items = 0
        if cart:
            for item in cart.items.select_related('artwork').all():
                artwork = item.artwork
                item_total = float(artwork.price) * item.quantity
                subtotal += item_total
                total_items += item.quantity
                items.append({
                    'artwork_id': artwork.id,
                    'name': artwork.name,
                    'price': float(artwork.price),
                    'quantity': item.quantity,
                    'total': item_total,
                    'framing_option': (
                        str(item.framing_condition)
                        if item.framing_condition else None
                    ),
                    'notes': item.notes,
                    'image_url': artwork.image_url if hasattr(
                        artwork, 'image_url'
                        ) else '',
                })
        return JsonResponse({
            'cart_uuid': str(cart.uuid) if cart else None,
            'items': items,
            'subtotal': round(subtotal, 2),
            'total_items': total_items,
        })
