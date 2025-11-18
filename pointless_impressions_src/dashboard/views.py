from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import EditOrderForm, OrderProcessingForm
from pointless_impressions_src.profiles.forms import SignupForm, AddressForm
from pointless_impressions_src.profiles.mixins import (
    ArtistRequiredMixin, StaffRequiredMixin
    )
from pointless_impressions_src.photo.forms import ProfilePhotoForm
from pointless_impressions_src.order.models import Order
from pointless_impressions_src.artwork.forms import ArtworkSubmissionForm
from pointless_impressions_src.account.models import CustomUser
from pointless_impressions_src.profiles.models import Artist
from pointless_impressions_src.artwork.models import Artwork
from pointless_impressions_src.order.forms import ApproveOrderForm
from pointless_impressions_src.artwork.forms import ArtworkApprovalForm


# Create your views here.
class DashboardLandingView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['access'] = {
            'user_profile': True,
            'artist': hasattr(user, 'artist'),
            'admin': (
                user.is_dashboard_admin
                or hasattr(user, 'staff_role')
                or user.groups.filter(
                    name__in=['Owner', 'Manager', 'Employee']
                ).exists()
            ),
            'django_admin': user.is_staff or user.is_superuser,
        }
        return context


class UserProfileDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_profile_dashboard.html'

    def get_context_data(self, **kwargs):
        public_id = self.kwargs.get('public_id')
        user = get_object_or_404(CustomUser, public_id=public_id)
        context = super().get_context_data(**kwargs)
        context['user_profile'] = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'profile_picture': (
                user.user_profile.profile_picture.url
                if user.user_profile.profile_picture else None
            ),
        }
        context['addresses'] = user.user_profile.customer.addresses.all()
        context['orders'] = user.user_profile.customer.orders.all()
        return context


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/includes/change_password_modal.html'
    form_class = SignupForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only include password fields
        form.fields = {
            key: form.fields[key]
            for key in ['password1', 'password2']
        }
        return form

    def form_valid(self, form):
        form.save(user=self.request.user)
        return JsonResponse({
            'success': True,
            'message': 'Password changed successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class EditUserInfoView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/includes/edit_user_info_modal.html'
    form_class = SignupForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude password fields
        for field in ['password1', 'password2']:
            form.fields.pop(field, None)
        return form

    def get_initial(self):
        user = self.request.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
        }

    def form_valid(self, form):
        form.save(user=self.request.user)
        return JsonResponse({
            'success': True,
            'message': 'User info updated successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class ChangeProfilePictureView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/includes/change_profile_pic_modal.html'
    form_class = ProfilePhotoForm

    def form_valid(self, form):
        form.save(user=self.request.user)
        return JsonResponse({
            'success': True,
            'message': 'Profile picture updated successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class CombinedOrderView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/including/order_modal.html'
    form_class = EditOrderForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(
            Order,
            id=order_id,
            customer=self.request.user.user_profile.customer
        )
        kwargs['artwork'] = (
            order.items.first().artwork if order.items.exists() else None
        )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = kwargs.get('order_id')
        order = get_object_or_404(
            Order,
            id=order_id,
            customer=self.request.user.user_profile.customer
        )
        context['order'] = order
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(
            Order,
            id=order_id,
            customer=self.request.user.user_profile.customer
        )
        form.save(order_id=order.id)
        return JsonResponse({
            'success': True,
            'message': 'Order updated successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class EditAddressView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/including/edit_address_modal.html'
    form_class = AddressForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        address_id = self.kwargs.get('address_id')
        if address_id:
            address = get_object_or_404(
                self.request.user.user_profile.customer.addresses,
                id=address_id
            )
            kwargs['instance'] = address
        else:
            kwargs['instance'] = None
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Address updated successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class ArtistDashboardView(ArtistRequiredMixin, TemplateView):
    template_name = 'dashboard/artist_dashboard.html'

    def get_context_data(self, **kwargs):
        public_id = self.kwargs.get('public_id')
        user = get_object_or_404(CustomUser, public_id=public_id)
        context = super().get_context_data(**kwargs)
        if hasattr(user, 'artist'):
            artist = user.artist
            context['artist'] = {
                'name': artist.name,
                'artworks': artist.artworks.all(),
                'sold_artworks': artist.artworks.filter(is_sold=True),
            }
        return context


class EditArtworkModalView(ArtistRequiredMixin, FormView):
    template_name = 'dashboard/includes/edit_artwork_modal.html'
    form_class = ArtworkSubmissionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        artwork_id = self.kwargs.get('artwork_id')
        kwargs['instance'] = get_object_or_404(
            Artwork, id=artwork_id, artist=self.request.user.artist
            )
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse(
            {'success': False, 'errors': form.errors}, status=400
        )

    def delete(self, request, *args, **kwargs):
        artwork_id = self.kwargs.get('artwork_id')
        artwork = get_object_or_404(
            Artwork, id=artwork_id, artist=self.request.user.artist
            )
        artwork.delete()
        return JsonResponse({'success': True})


class AddArtworkModalView(ArtistRequiredMixin, FormView):
    template_name = 'dashboard/includes/add_artwork_modal.html'
    form_class = ArtworkSubmissionForm

    def form_valid(self, form):
        artwork = form.save(commit=False)
        artwork.artist = self.request.user.artist
        artwork.save()
        form.save_m2m()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse(
            {'success': False, 'errors': form.errors}, status=400
        )


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Define access levels based on roles
        context['access'] = {
            'order_processing': True,
            'artist_requests': user.groups.filter(
                name__in=['Owner', 'Manager', 'Employee']
            ).exists(),
            'artwork_submissions': True,
            'artwork_removal': user.groups.filter(
                name__in=['Owner', 'Manager']
            ).exists(),
            'authentication_resolutions': True,
            'manage_admins': user.groups.filter(name='Owner').exists(),
            'block_ban_users': True,
            'manage_refunds': True,
            'pay_artists': user.groups.filter(
                name__in=['Owner', 'Manager']
            ).exists(),
            'write_blogs': True,
        }

        # Add additional context for dashboard functionality
        context['orders'] = Order.objects.filter(status='pending')
        context['artist_applications'] = Artist.objects.filter(
            is_approved=False
        )
        context['artwork_submissions'] = Artwork.objects.filter(
            is_available=False
        )

        return context


class ApproveOrderView(ArtistRequiredMixin, FormView):
    template_name = 'dashboard/includes/approve_order_modal.html'
    form_class = ApproveOrderForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        order_id = self.kwargs.get('order_id')
        kwargs['instance'] = get_object_or_404(
            Order, id=order_id, status='pending'
        )
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Order approved successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class OrderProcessingView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/order_processing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(status='pending')
        return context


class OrderProcessingModalView(StaffRequiredMixin, FormView):
    template_name = 'dashboard/includes/order_processing_modal.html'
    form_class = OrderProcessingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        order_id = self.kwargs.get('order_id')
        kwargs['instance'] = get_object_or_404(Order, id=order_id)
        return kwargs

    def form_valid(self, form):
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Order processed successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class ManageArtistsView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/manage_artists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()
        return context


class ArtworkApprovalView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/artwork_approval.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artworks'] = Artwork.objects.filter(is_available=False)
        for artwork in context['artworks']:
            artwork.approval_form = ArtworkApprovalForm(instance=artwork)
        return context

    def post(self, request, *args, **kwargs):
        artwork_id = kwargs.get('artwork_id')
        artwork = get_object_or_404(Artwork, id=artwork_id)
        form = ArtworkApprovalForm(request.POST, instance=artwork)
        if form.is_valid():
            artwork = form.save(commit=False)
            action = request.POST.get('action')
            if action == 'approve':
                artwork.is_available = True
            elif action == 'reject':
                artwork.is_available = False
                artwork.rejection_notes = request.POST.get(
                    'rejection_notes', ''
                )
            artwork.save()
            return JsonResponse({'success': True})
        return JsonResponse(
            {'success': False, 'errors': form.errors},
            status=400
            )
