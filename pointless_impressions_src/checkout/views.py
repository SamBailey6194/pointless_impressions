import json
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib import messages
from pointless_impressions_src.artwork.models import Artwork
from .forms import (
    AddToCartForm,
    UpdateCartQuantityForm,
    RemoveFromCartForm,
    SyncCartForm,
)


class CartAPIView(View):
    """Base class for cart API endpoints"""

    def get_cart_from_session(self):
        """Get cart from session or initialize empty dict"""
        return self.request.session.get('cart', {})

    def save_cart_to_session(self, cart):
        """Save cart to session"""
        self.request.session['cart'] = cart
        self.request.session.modified = True

    def get_cart_count(self):
        """Get total quantity of items in cart"""
        cart = self.get_cart_from_session()
        return sum(item.get('quantity', 0) for item in cart.values())


@method_decorator(require_http_methods(['POST']), name='dispatch')
class AddToCartView(CartAPIView):
    """
    POST /checkout/api/cart/add/
    Add item to cart

    Required POST data:
    - artwork_id: int
    - quantity: int (1-999)

    Optional POST data:
    - framing_option: int
    - notes: str (max 500 chars)

    Response: {success: bool, cart_count: int, message: str}
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

        # SECURITY: Validate artwork is in stock (SSR protection)
        if not artwork.is_in_stock or not artwork.is_available:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'This artwork is no longer available',
                    'type': 'error',
                },
                status=400
            )

        # Get or initialize cart from session
        cart = self.get_cart_from_session()

        # Add or update cart item
        artwork_key = str(artwork_id)
        if artwork_key in cart:
            new_quantity = cart[artwork_key]['quantity'] + quantity
        else:
            new_quantity = quantity

        # SECURITY: Validate total quantity doesn't exceed stock
        if new_quantity > artwork.quantity:
            return JsonResponse(
                {
                    'success': False,
                    'message': f'Only {artwork.quantity} units available',
                    'type': 'error',
                },
                status=400
            )

        # Update cart
        if artwork_key in cart:
            cart[artwork_key]['quantity'] = new_quantity
        else:
            cart[artwork_key] = {
                'id': artwork_id,
                'name': artwork.name,
                'price': float(artwork.price),
                'quantity': quantity,
                'slug': artwork.slug,
            }

            # Add optional fields if provided
            if framing_option:
                cart[artwork_key]['framing_option'] = framing_option
            if notes:
                cart[artwork_key]['notes'] = notes

        # Save cart to session
        self.save_cart_to_session(cart)

        # Add Django message for SSR (page reload) and API response
        message_text = f'{artwork.name} added to cart'
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_count': self.get_cart_count(),
                'cart': cart,
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
        artwork_key = str(artwork_id)

        cart = self.get_cart_from_session()

        if artwork_key not in cart:
            return JsonResponse(
                {'success': False, 'message': 'Item not in cart'},
                status=404
            )

        del cart[artwork_key]
        self.save_cart_to_session(cart)

        # Add Django message
        message_text = 'Item removed from cart'
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_count': self.get_cart_count(),
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
        artwork_key = str(artwork_id)

        cart = self.get_cart_from_session()

        if artwork_key not in cart:
            return JsonResponse(
                {'success': False, 'message': 'Item not in cart'},
                status=404
            )

        # Get artwork to validate against stock
        try:
            artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Artwork not found'},
                status=404
            )

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
            del cart[artwork_key]
            message_text = 'Item removed from cart'
        else:
            # SECURITY: Validate quantity against stock
            if not artwork.is_in_stock or not artwork.is_available:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'This artwork is no longer available',
                        'type': 'error',
                    },
                    status=400
                )

            if quantity > artwork.quantity:
                return JsonResponse(
                    {
                        'success': False,
                        'message': f'Only {artwork.quantity} units available',
                        'type': 'error',
                    },
                    status=400
                )

            cart[artwork_key]['quantity'] = quantity
            message_text = 'Cart updated'

        self.save_cart_to_session(cart)

        # Add Django message
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_count': self.get_cart_count(),
            },
            status=200
        )


@method_decorator(require_http_methods(['POST']), name='dispatch')
class SyncCartView(CartAPIView):
    """
    POST /checkout/api/cart/sync/
    Sync localStorage cart with backend session

    Required JSON body:
    {
      "cart": {
        "artwork_id": {
          "id": int,
          "name": str,
          "price": float,
          "quantity": int
        }
      }
    }

    Response: {success: bool, cart_count: int, message: str}
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

        cart = form.cleaned_data['cart']

        # Validate all artwork IDs exist
        for artwork_id in cart.keys():
            try:
                Artwork.objects.get(id=artwork_id)
            except Artwork.DoesNotExist:
                return JsonResponse(
                    {
                        'success': False,
                        'message': f'Artwork {artwork_id} not found',
                    },
                    status=404
                )

        # Save synced cart to session
        self.save_cart_to_session(cart)

        # Add Django message
        message_text = 'Cart synced'
        messages.success(request, message_text)

        return JsonResponse(
            {
                'success': True,
                'message': message_text,
                'type': 'success',
                'cart_count': self.get_cart_count(),
            },
            status=200
        )
