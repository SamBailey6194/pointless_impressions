from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import json
import uuid
import os
import hmac
import hashlib
import base64
from .models import Order
from .utils import create_order_from_cart
from .forms import OrderForm
from pointless_impressions_src.cart.utils import get_cart
from square.client import Square
from square.environment import SquareEnvironment

# Create your views here.
square_client = Square(
    token=os.getenv('SQUARE_ACCESS_TOKEN'),
    environment=SquareEnvironment.SANDBOX
)


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
        print('Processing order confirmation...')
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {
                    'status': 'error', 'message': 'Invalid request method'
                }, status=400)

        print('Received AJAX request for order confirmation.')

        try:
            data = json.loads(request.body)
            source_id = data.get('sourceId')
            form_data = data.get('formData', {})

            cart = get_cart(request)

            if not cart or cart.get_total_quantity() == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': (
                        "Your cart is empty or expired. "
                        "Please add items before placing an order."
                        )
                }, status=400)

            form = OrderForm(data=form_data, user=request.user)

            if not form.is_valid():
                return JsonResponse({
                    'status': 'error',
                    'message': "Please correct the errors in your "
                    "address form."
                }, status=400)

            grand_total = cart.get_grand_total()
            amount_in_pence = int(grand_total * 100)

            print('Payment details prepared:')

            try:
                payment_response = square_client.payments.create(
                    source_id=source_id,
                    idempotency_key=str(uuid.uuid4()),
                    amount_money={
                        "amount": amount_in_pence,
                        "currency": "GBP"
                    },
                    location_id=os.getenv('SQUARE_LOCATION_ID'),
                    note=f"Order for {form.cleaned_data.get('email')}",
                    buyer_email_address=form.cleaned_data.get('email'),
                )

                print(f'Payment created: {payment_response}')
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f"Payment processing error: {str(e)}"
                }, status=500)

            if payment_response.errors:
                error_msg = payment_response.errors[0].get(
                    'detail', 'Payment processing failed.'
                    )
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=400)
            elif payment_response.errors is None:
                payment_result = payment_response.payment

                cleaned_data = form.cleaned_data

                shipping_address_snapshot = self.build_address_snapshot(
                    cleaned_data, "shipping"
                )
                billing_address_snapshot = self.build_address_snapshot(
                    cleaned_data, "billing"
                )

                order_data = {
                    'email': cleaned_data.get('email') or (
                        request.user.email if
                        request.user.is_authenticated
                        else None
                    ),
                    'phone': cleaned_data.get('phone'),
                    'shipping_address': shipping_address_snapshot,
                    'billing_address': billing_address_snapshot,
                    'payment_id': payment_result.id
                }

                try:
                    new_order = create_order_from_cart(cart, order_data)
                    new_order.payment_id = payment_result.id
                    new_order.save()

                    if 'cart_id' in request.session:
                        del request.session['cart_id']

                    request.session['recent_order_id'] = str(new_order.id)

                    return JsonResponse({
                        'status': 'success',
                        'redirect_url': reverse(
                            'orders:order_success',
                            args=[new_order.id]
                        )
                    })
                except Exception as e:
                    return JsonResponse({
                        'status': 'error',
                        'message': f"Order creation failed: {str(e)}"
                        }, status=500)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': (
                        "Payment processing failed. "
                        "Please check your payment details and try again."
                    )
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"An error occurred: {str(e)}"
            }, status=500)

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

        is_dashboard_admin = False
        order_owner = False
        if request.user.is_authenticated:
            is_dashboard_admin = getattr(
                request.user, 'is_dashboard_admin', False
            )
            order_owner = (order.user == request.user)

        is_in_session = (str(order.id) == session_order_id)

        if not (is_dashboard_admin or order_owner or is_in_session):
            messages.error(request, _(
                "You do not have permission to view this order."
            ))
            return redirect('home')

        if 'recent_order_id' in request.session:
            del request.session['recent_order_id']

        context = {
            'order': order
        }

        return render(request, self.template_name, context)


@method_decorator(csrf_exempt, name='dispatch')
class SquareWebhookView(View):
    def post(self, request, *args, **kwargs):
        print('Received Square webhook notification.')
        print('Incoming webhook headers:', request.headers)
        print('Incoming webhook body:', request.body.decode('utf-8'))
        print('Incoming webhook host:', request.get_host())

        signature = request.headers.get('x-square-hmacsha256-signature')
        body = request.body.decode('utf-8')
        notification_url = os.getenv('SQUARE_WEBHOOK_URL')
        signature_key = os.getenv('SQUARE_WEBHOOK_SIGNATURE_KEY')
        subscription_id = request.headers.get('Square-Subscription-Id')

        print("Square:", signature)
        print("URL used:", notification_url)
        print("BODY:", body)

        # Compute the HMAC-SHA256 signature
        computed_signature = base64.b64encode(
            hmac.new(
                signature_key.encode('utf-8'),
                f"{notification_url}{body}".encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')

        print("Computed:", computed_signature)

        # Compare the computed signature with the Square signature
        if not hmac.compare_digest(computed_signature, signature):
            return HttpResponse("Invalid Signature", status=403)

        try:
            event = json.loads(body)
            event_subscription_id = subscription_id
            expected_subscription_id = os.getenv(
                'SQUARE_WEBHOOK_SUBSCRIPTION_ID'
                )

            print("Event Subscription ID:", event_subscription_id)
            print("Expected Subscription ID:", expected_subscription_id)
            if event_subscription_id != expected_subscription_id:
                return HttpResponse("Invalid Subscription ID", status=403)

            if event.get('type') == 'payment.updated':
                payment_data = event['data']['object']['payment']
                square_id = payment_data['id']
                status = payment_data['status']

                try:
                    order = Order.objects.get(payment_id=square_id)
                    order.status = status
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponse("Order Not Found", status=404)
            print("Event Type Processed:", event.get('type'))
            print("Webhook processing completed.")
            return HttpResponse("OK", status=200)
        except Exception as e:
            print(f"Webhook Error: {e}")
            return HttpResponse("Error", status=200)
