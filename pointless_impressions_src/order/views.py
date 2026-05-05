from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import json
import uuid
import os
import hmac
import hashlib
import base64
from .models import Order, PaymentRecovery
from .utils import (
    create_order_from_cart,
    build_address_dict,
    send_order_confirmation_email
    )
from .forms import OrderForm
from pointless_impressions_src.cart.utils import get_cart, serialize_items
from square.client import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError

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
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(
                {
                    'status': 'error', 'message': 'Invalid request method'
                }, status=400)

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

            form = OrderForm(data=form_data)

            if not form.is_valid():
                return JsonResponse({
                    'status': 'error',
                    'message': "Please correct the errors in your "
                    "address form."
                }, status=400)

            grand_total = cart.get_grand_total()
            amount_in_pence = int(grand_total * 100)
            payment_id = None
            payment_result = None

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
            except ApiError as e:
                detail = e.errors[0].detail if e.errors else None
                error_msg = (
                    detail or
                    'Card verification failed. Please try a different card.'
                )
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=400)
            except Exception:
                return JsonResponse({
                    'status': 'error',
                    'message': "Payment processing error. Please try again."
                }, status=500)

            if payment_response.errors:
                error = payment_response.errors[0]
                error_msg = (
                    error.detail or
                    'Payment processing failed. Please try again.'
                )
                return JsonResponse({
                    'status': 'error',
                    'message': error_msg
                }, status=400)

            payment_result = payment_response.payment
            payment_id = payment_result.id

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
                'payment_id': payment_id
            }

            try:
                new_order = create_order_from_cart(cart, order_data)
                new_order.payment_id = payment_id
                new_order.save()

                try:
                    send_order_confirmation_email(new_order)
                except Exception as e:
                    import traceback
                    print("Failed to send order confirmation email:", e)
                    print(traceback.format_exc())

                if 'cart_id' in request.session:
                    del request.session['cart_id']

                request.session['recent_order_id'] = str(new_order.id)

                return JsonResponse({
                    'status': 'success',
                    'redirect_url': reverse(
                        'orders:order_success',
                        args=[new_order.id]
                    ),
                    'message': "Order placed successfully. "
                    "Check your email for order confirmation."
                })
            except Exception:
                return JsonResponse({
                    'status': 'error',
                    'message': "Order creation failed. Please contact support."
                    }, status=500)

        except Exception:
            try:
                payment_id_recovery = (
                    payment_result.id
                    if 'payment_result' in dir() and payment_result
                    else None
                )
                shipping_snapshot = self.build_address_snapshot(
                    form_data, 'shipping'
                )
                billing_snapshot = self.build_address_snapshot(
                    form_data, 'billing'
                )
                PaymentRecovery.objects.create(
                    payment_id=payment_id_recovery,
                    amount=cart.get_grand_total(),
                    currency='GBP',
                    buyer_email=form_data.get('email'),
                    buyer_phone=form_data.get('phone'),
                    billing_address=build_address_dict(billing_snapshot),
                    shipping_address=build_address_dict(shipping_snapshot),
                    cart_snapshot=serialize_items(cart),
                    notes="Order creation failed."
                )
            except Exception:
                pass
            return JsonResponse({
                'status': 'error',
                'message': "An error occurred while processing your order. "
                "Please try again later."
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
        retry_number = request.headers.get('Square-Retry-Number')
        if retry_number and int(retry_number) > 0:
            print(
                f"Retry attempt #{retry_number} detected. "
                "Ignoring duplicate webhook."
                )
            return HttpResponse("OK", status=200)

        signature = request.headers.get('x-square-hmacsha256-signature')
        body = request.body.decode('utf-8')
        notification_url = os.getenv('SQUARE_WEBHOOK_URL')
        signature_key = os.getenv('SQUARE_WEBHOOK_SIGNATURE_KEY')
        subscription_id = request.headers.get('Square-Subscription-Id')

        # Compute the HMAC-SHA256 signature
        computed_signature = base64.b64encode(
            hmac.new(
                signature_key.encode('utf-8'),
                f"{notification_url}{body}".encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')

        # Compare the computed signature with the Square signature
        if not hmac.compare_digest(computed_signature, signature):
            return HttpResponse("Invalid Signature", status=403)

        try:
            event = json.loads(body)
            event_subscription_id = subscription_id
            expected_subscription_id = os.getenv(
                'SQUARE_WEBHOOK_SUBSCRIPTION_ID'
                )

            if event_subscription_id != expected_subscription_id:
                return HttpResponse("Invalid Subscription ID", status=403)

            if event.get('type') == 'payment.updated':
                payment_data = event['data']['object']['payment']
                square_id = payment_data['id']
                status = payment_data['status']
                line_items = payment_data.get(
                    'order', {}
                    ).get('line_items', [])

                cart_snapshot = []
                for item in line_items:
                    cart_snapshot.append({
                        'item_name': item.get('name'),
                        'quantity': int(item.get('quantity', '1')),
                        'price_at_purchase': Decimal(
                            item.get('base_price_money', {}).get('amount', 0)
                            ) / 100,
                        'currency': (
                            item.get(
                                'base_price_money', {}
                                ).get('currency', 'GBP')
                            )
                    })

                try:
                    order = Order.objects.get(payment_id=square_id)
                    order.status = status
                    order.save()
                except Order.DoesNotExist:
                    payment_recovered, _ = (
                        PaymentRecovery.objects.get_or_create(
                            payment_id=square_id,
                            defaults={
                                'amount': Decimal(
                                    payment_data['total_money']['amount']
                                    ) / 100,
                                'currency': (
                                    payment_data['total_money']['currency']
                                    ),
                                'buyer_email': payment_data.get(
                                    'buyer_email_address', ''
                                    ),
                                'buyer_phone': payment_data.get(
                                    'buyer_phone_number', ''
                                    ),
                                'billing_address': build_address_dict(
                                    payment_data.get('billing_address', {})
                                    ),
                                'shipping_address': build_address_dict(
                                    payment_data.get('shipping_address', {})
                                    ),
                                'cart_snapshot': cart_snapshot,
                                'notes': f"Recovered from webhook event "
                                f"{event.get('id')}"
                            }
                        )
                    )
                    payment_recovered.save()
                    return HttpResponse("Ok", status=200)
            return HttpResponse("OK", status=200)
        except Exception:
            return HttpResponse("Error", status=200)
