from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from .models import Cart
from pointless_impressions_src.artwork.models import Artwork
import logging

logger = logging.getLogger(__name__)


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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the cart for the current user or anonymous session
        cart = None
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(
                user=self.request.user, is_active=True
            ).first()
        else:
            sessionid = self.request.COOKIES.get('sessionid')
            if sessionid:
                cart = Cart.objects.filter(
                    session_id=sessionid, is_active=True
                ).first()

        # Prepare cart items and totals
        cart_items = []
        total_price = 0
        total_quantity = 0

        if cart:
            for item in cart.items.select_related(
                'artwork', 'framing_condition'
            ).all():
                item_total = float(item.artwork.price) * item.quantity
                total_price += item_total
                total_quantity += item.quantity

                cart_items.append({
                    'artwork': item.artwork,
                    'quantity': item.quantity,
                    'price': float(item.artwork.price),
                    'total': item_total,
                    'framing_option': item.framing_condition,
                })

        # Update the context with cart data
        context.update({
            'cart_items': cart_items,
            'total_price': total_price,
            'total_quantity': total_quantity,
        })

        return context


class CartDropdownView(View):
    def get(self, request, *args, **kwargs):
        session_id = request.session.session_key
        logger.debug(f"Fetching cart for session_id: {session_id}")
        print(f"Fetching cart for session_id: {session_id}")

        # Fetch the cart using the session key
        cart = Cart.objects.filter(
            session_id=session_id, is_active=True
        ).first()
        logger.debug(f"Cart fetched: {cart}")
        print(f"Cart fetched: {cart}")

        cart_items = []
        total_quantity = 0
        total_price = 0
        if cart and cart.data:
            artwork_ids = list(cart.data.keys())
            artworks = Artwork.objects.filter(id__in=artwork_ids).in_bulk()
            logger.debug(f"Artworks fetched for cart items: {artworks}")
            print(f"Artworks fetched for cart items: {artworks}")

            for artwork_id, item in cart.data.items():
                artwork = artworks.get(int(artwork_id))
                if artwork:
                    cart_items.append({
                        "artwork": artwork,
                        "quantity": item.get("quantity", 0),
                        "notes": item.get("notes", ""),
                        "price": item.get("price", 0),
                    })
                    total_quantity += item.get("quantity", 0)
                    total_price += (
                        item.get("quantity", 0) * item.get("price", 0)
                        )
                else:
                    logger.debug(f"Artwork with ID {artwork_id} not found.")
                    print(f"Artwork with ID {artwork_id} not found.")

        html = render_to_string(
            "checkout/includes/cart_dropdown.html",
            {
                "cart_items": cart_items,
                "total_quantity": total_quantity,
                "total_price": total_price
            }
        )
        logger.debug("Cart dropdown HTML rendered successfully")
        print("Cart dropdown HTML rendered successfully")
        return JsonResponse({"html": html})
