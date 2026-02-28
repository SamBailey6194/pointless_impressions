from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EditOrderForm
from .mixins import AdminRequiredMixin
from pointless_impressions_src.account.models import CustomUser
from pointless_impressions_src.artwork.forms import ArtworkSubmissionForm
from pointless_impressions_src.artwork.models import Artwork
from pointless_impressions_src.order.models import Order


# Create your views here.
class DashboardLandingView(LoginRequiredMixin, TemplateView):
    """
    Dsahboard landing view that provides access control context.

    GET: Renders the dashboard landing page with user access context.

    Context:
        access (dict): A dictionary indicating user access levels.
            - user_profile (bool): Access to user profile dashboard.
            - admin (bool): Access to admin dashboard.

    Template:
        dashboard/landing.html

    Methods:
        get_context_data(**kwargs): Adds access control context based on user
        roles.
    """
    template_name = 'dashboard/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(f"Current user: {self.request.user}")
        print(f"User groups: {self.request.user.groups.all()}")
        context['access'] = {
            'user_profile': True,
            'admin': (
                user.is_dashboard_admin
                or hasattr(user, 'staff_role')
                or user.groups.filter(
                    name__in=['Owner', 'Manager', 'Employee']
                ).exists()
            ),
        }
        return context


class UserProfileDashboardView(LoginRequiredMixin, TemplateView):
    """
    User profile dashboard view displaying user information.

    GET: Renders the user profile dashboard page with user details.

    Context:
        user_profile (CustomUser): The user whose profile is being viewed.
        profile_photo (UserPhoto): The profile photo of the user.
        addresses (QuerySet): The addresses associated with the user's profile.
        orders (QuerySet): The orders associated with the user.

    Template:
        dashboard/user_profile_dashboard.html
    """
    template_name = 'dashboard/user_profile_dashboard.html'

    def get_context_data(self, **kwargs):
        public_id = self.kwargs.get('public_id')
        user = get_object_or_404(CustomUser, public_id=public_id)
        context = super().get_context_data(**kwargs)

        profile_photo = user.user_profile.photos.filter(
            photo_type='profile'
        ).first()

        context['user_profile'] = user
        context['profile_photo'] = profile_photo
        context['addresses'] = user.user_profile.customer.addresses.all()
        context['orders'] = user.orders.exclude(
            status='CANCELLED'
        ).order_by('-order_number')
        return context


class EditArtworkModalView(AdminRequiredMixin, FormView):
    """
    Modal view for editing existing artwork details.

    GET: Renders the edit artwork modal form.

    Form:
        ArtworkSubmissionForm: Form for editing artwork details.
        Form is pre-populated with existing artwork data.

    POST: Processes the submitted form to update artwork details.

    Template:
        dashboard/includes/edit_artwork_modal.html
    """
    template_name = 'dashboard/includes/edit_artwork_modal.html'
    form_class = ArtworkSubmissionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        slug = self.kwargs.get('artwork_slug')

        if slug:
            artwork = get_object_or_404(Artwork, slug=slug)
            kwargs['instance'] = artwork
        else:
            kwargs['instance'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('artwork_slug')

        if slug:

            context['artwork'] = get_object_or_404(Artwork, slug=slug)

        context['artwork_submission_form'] = context['form']
        return context

    def form_valid(self, form):
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Artwork updated successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class AddArtworkModalView(AdminRequiredMixin, FormView):
    """
    Modal view for adding new artwork submissions.

    GET: Renders the add artwork modal form.

    POST: Processes the submitted form to create a new artwork.

    Form:
        ArtworkSubmissionForm: Form for submitting new artwork details.
        Form is empty for new submissions.

    Template:
        dashboard/includes/add_artwork_modal.html
    """
    template_name = 'dashboard/includes/add_artwork_modal.html'
    form_class = ArtworkSubmissionForm

    def form_valid(self, form):
        artist = None

        if hasattr(self.request.user, 'user_profile'):
            if hasattr(self.request.user.user_profile, 'artist'):
                artist = self.request.user.user_profile.artist

        form.save(artist=artist)

        return JsonResponse({
            'success': True,
            'message': 'Artwork added successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """
    Admin dashboard view for managing artwork submissions.

    GET: Renders the admin dashboard with artwork management context.

    Context:
        access (dict): A dictionary indicating admin access levels.
            - artwork_submissions (bool): Access to manage artwork submissions.
            - artwork_removal (bool): Access to remove artwork submissions.

    Template:
        dashboard/admin_dashboard.html
    """
    template_name = 'dashboard/admin_dashboard.html'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_artworks = Artwork.objects.all().order_by('-created_at')
        artwork_page = self.request.GET.get('artwork_page', 1)
        artwork_paginator = Paginator(all_artworks, 15)

        try:
            artworks = artwork_paginator.page(artwork_page)
        except PageNotAnInteger:
            artworks = artwork_paginator.page(1)
        except EmptyPage:
            artworks = artwork_paginator.page(artwork_paginator.num_pages)

        context['artworks'] = artworks
        context['artwork_page_obj'] = artworks
        context['artwork_is_paginated'] = artwork_paginator.num_pages > 1

        context['artwork_submission_form'] = ArtworkSubmissionForm()

        all_orders = Order.objects.all().order_by('-order_number')
        order_page = self.request.GET.get('order_page', 1)
        order_paginator = Paginator(all_orders, 15)

        try:
            orders = order_paginator.page(order_page)
        except PageNotAnInteger:
            orders = order_paginator.page(1)
        except EmptyPage:
            orders = order_paginator.page(order_paginator.num_pages)

        context['orders'] = orders
        context['order_page_obj'] = orders
        context['order_is_paginated'] = order_paginator.num_pages > 1

        return context


class GuestOrderView(View):
    """
    View for guest users to access their order details securely.

    GET: Renders the guest order page if access token is valid and referrer
        is from the email link.

    Context:
        order (Order): The guest order being viewed.
        featured_artworks (QuerySet): A list of featured artworks to display.

    Template:
        dashboard/guest_order.html
    """
    def get(self, request, order_id):
        access_code = request.GET.get('access_code')
        session_key = f'guest_order_{order_id}'

        try:
            order = Order.objects.get(id=order_id, user=None)
        except Order.DoesNotExist:
            raise Http404("Order does not exist.")

        if access_code:
            if order.guest_access_code != access_code:
                raise PermissionDenied("Invalid access token.")
            request.session[session_key] = access_code
        elif request.session.get(session_key) == order.guest_access_code:
            pass
        else:
            raise PermissionDenied("Access token required.")

        featured_artworks = Artwork.objects.filter(is_featured=True)[:10]

        return render(request, 'dashboard/guest_order.html', {
            'order': order,
            'featured_artworks': featured_artworks,
        })


class UpdateOrderView(LoginRequiredMixin, View):
    """
    View to handle updating an order.

    POST: Updates the order details based on the provided data.
    Returns the updated order details.

    Context:
        order (Order): The order being updated.
    """
    template_name = 'dashboard/includes/update_order_modal.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        form = EditOrderForm(instance=order)

        return render(
            request, 'dashboard/includes/update_order_modal.html',
            {'order_form': form, 'order_id': order_id}
        )

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=request.user)
        form = EditOrderForm(request.POST, instance=order)

        self._remove_fields(form)

        if form.is_valid():
            form.save()

            updated_shipping_address = (
                f"{order.shipping_first_name} {order.shipping_last_name}, "
                f"{order.shipping_address_line_1}, "
                f"{order.shipping_address_line_2 or ''}, "
                f"{order.shipping_city}, {order.shipping_postcode}"
            )

            updated_billing_address = (
                f"{order.billing_first_name} {order.billing_last_name}, "
                f"{order.billing_address_line_1}, "
                f"{order.billing_address_line_2 or ''}, "
                f"{order.billing_city}, {order.billing_postcode}"
            )

            return JsonResponse({
                'success': True,
                'message': 'Order updated successfully.',
                'updated_shipping_address': updated_shipping_address,
                'updated_billing_address': updated_billing_address,
            })

        return JsonResponse({
            'success': False,
            'message': 'Failed to update order.',
            'errors': form.errors,
        })

    def _remove_fields(self, form):
        """Helper method to remove fields consistently"""
        if 'email' in form.fields:
            del form.fields['email']
        if 'phone' in form.fields:
            del form.fields['phone']


class DeleteOrderView(LoginRequiredMixin, View):
    """
    View to handle updating an order.

    POST: Updates the order details based on the provided data.
    Returns the updated order details.

    Context:
        order (Order): The order being updated.
    """
    template_name = 'dashboard/includes/delete_order_modal.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(
            request, 'dashboard/includes/delete_order_modal.html',
            {'order': order, 'order_id': order_id}
        )

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        try:
            order.delete()
            return JsonResponse(
                {'success': True, 'message': 'Order deleted successfully.'}
            )
        except Exception as e:
            return JsonResponse(
                {'success': False, 'message': str(e)}, status=400
            )


class DeleteArtworkModalView(AdminRequiredMixin, View):
    """
    Modal view for deleting artwork.
    """
    template_name = 'dashboard/includes/delete_artwork_modal.html'

    def get(self, request, artwork_slug, *args, **kwargs):
        artwork = get_object_or_404(Artwork, slug=artwork_slug)
        return render(
            request, self.template_name,
            {'artwork': artwork}
        )

    def post(self, request, artwork_slug, *args, **kwargs):
        artwork = get_object_or_404(Artwork, slug=artwork_slug)
        try:
            artwork_name = artwork.name
            artwork.delete()
            return JsonResponse({
                'success': True,
                'message': f'Artwork "{artwork_name}" deleted successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)


class EditOrderModalView(AdminRequiredMixin, View):
    """
    Modal view for editing orders.
    """
    template_name = 'dashboard/includes/edit_order_modal.html'

    def get(self, request, public_id, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = EditOrderForm(instance=order)
        return render(
            request, self.template_name,
            {
                'order_form': form,
                'order': order,
                'order_id': order_id
            }
        )

    def post(self, request, public_id, order_id):
        order = get_object_or_404(Order, id=order_id)
        form = EditOrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Order updated successfully.'
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class DeleteOrderModalView(AdminRequiredMixin, View):
    """
    Modal view for deleting orders.
    """
    template_name = 'dashboard/includes/delete_order_modal.html'

    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        return render(
            request, self.template_name,
            {'order': order, 'order_id': order_id}
        )

    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        try:
            order_number = order.order_number
            order.delete()
            return JsonResponse({
                'success': True,
                'message': f'Order #{order_number} deleted successfully.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
