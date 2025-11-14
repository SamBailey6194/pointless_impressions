from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Order
from .utils import create_order_from_cart
from .forms import OrderForm
from pointless_impressions_src.cart.utils import get_cart
from pointless_impressions_src.artwork.models import Artwork


# Create your views here.
class OrderConfirmationView(View):
    """
    This view handles the order confirmed:

    It's a backend view that processes the order after payment
    has been successfully made.

    Methods:
    - post: Process the order confirmation form submission

    Protection:
    - Ensures the cart is valid and has items
    - Validates the order form data
    - Handles payment processing errors gracefully
    - Ensures the order is created successfully
    - Ensures the order is only viewable by authorized users

    Context Data:
    - N/A (redirects on success/failure)

    Response: Redirects to order success page or back to checkout on failure
    """
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)

        if not cart or cart.get_total_quantity() == 0:
            messages.error(request, _("Your cart is empty or has expired."))
            return redirect('cart:checkout')

        form = OrderForm(request.POST, user=request.user)

        if not form.is_valid():
            messages.error(request, _(
                "Please correct the errors in your address form."
                ))
            return redirect('cart:checkout')

        try:
            # ---
            # YOUR PAYMENT LOGIC GOES HERE
            # e.g., stripe.Charge.create(...)
            # ---
            payment_success = True

        except Exception as e:
            messages.error(request, _(
                f"Your payment could not be processed: {str(e)}"
                ))
            return redirect('cart:checkout')

        if payment_success:
            form_data = form.cleaned_data

            shipping_address_snapshot = self.build_address_snapshot(
                form_data, "shipping"
                )

            billing_address_snapshot = self.build_address_snapshot(
                form_data, "billing"
                )

            order_data = {
                'email': form_data.get('email') or (
                    request.user.email if
                    request.user.is_authenticated
                    else None
                    ),
                'phone': form_data.get('phone'),
                'shipping_address': shipping_address_snapshot,
                'billing_address': billing_address_snapshot,
            }

            try:
                new_order = create_order_from_cart(cart, order_data)
            except Exception as e:
                messages.error(request, _(
                    f"There was an error creating your order. "
                    f"Please contact support. Error: {str(e)}"
                    ))
                return redirect('cart:checkout')

            if 'cart_id' in request.session:
                del request.session['cart_id']

            messages.success(request, _(
                "Your order has been successfully placed!"
                ))

            request.session['recent_order_id'] = str(new_order.id)

            return redirect('orders:order_success', order_id=new_order.id)

        messages.error(request, _(
            "An unknown error occurred. Please try again."
            ))
        return redirect('cart:checkout')

    def build_address_snapshot(self, form_data, prefix):
        """Helper to build the address dictionary from form fields."""
        return {
            f"{prefix}_first_name": form_data[
                f"{prefix}_first_name"
                ],
            f"{prefix}_last_name": form_data[f"{prefix}_last_name"],
            f"{prefix}_address_line_1": form_data[f"{prefix}_address_line_1"],
            f"{prefix}_address_line_2": form_data.get(
                f"{prefix}_address_line_2", ""
            ),
            f"{prefix}_city": form_data[f"{prefix}_city"],
            f"{prefix}_county": form_data.get(f"{prefix}_county", ""),
            f"{prefix}_postcode": form_data[f"{prefix}_postcode"],
            f"{prefix}_country": form_data[f"{prefix}_country"],
        }


class OrderSuccessView(View):
    """
    View to display order success confirmation page

    GET /order/success/<order_id>/

    Displays the order confirmation page with order details.

    Protection:
    - Only the order owner, dashboard admins, or users with
      the order ID in their session can view the order.

    Context Data:
    - order: The Order object containing all order details.

    Response: Renders order_confirmation.html template with order context
    """
    template_name = 'order/order_confirmation.html'

    def get(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id
        )

        session_order_id = request.session.get('recent_order_id')

        is_dashbaord_admin = False
        order_owner = False
        if request.user.is_authenticated:
            is_dashbaord_admin = getattr(
                request.user, 'is_dashboard_admin', False
                )
            order_owner = (order.user == request.user)

        is_in_session = (str(order.id) == session_order_id)

        if not (is_dashbaord_admin or order_owner or is_in_session):
            messages.error(request, _(
                "You do not have permission to view this order."
                ))
            return redirect('home')

        if 'recent_order_id' in request.session:
            del request.session['recent_order_id']

        context = {
            'order': order
        }

        context['featured_artworks'] = Artwork.objects.filter(
            is_featured=True
            ).select_related(
                'main_photo',
                'artist__user',
                'category'
            ).prefetch_related(
                'selected_conditions'
            )[:10]

        return render(request, self.template_name, context)
