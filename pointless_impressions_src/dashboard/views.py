from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from pointless_impressions_src.profiles.mixins import StaffRequiredMixin
from pointless_impressions_src.account.models import CustomUser
from pointless_impressions_src.artwork.forms import ArtworkSubmissionForm
from pointless_impressions_src.artwork.models import Artwork


# Create your views here.
class DashboardLandingView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
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
        context['orders'] = user.orders.all()
        return context


class EditArtworkModalView(StaffRequiredMixin, FormView):
    template_name = 'dashboard/includes/edit_artwork_modal.html'
    form_class = ArtworkSubmissionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        artwork_id = self.kwargs.get('artwork_id')
        if artwork_id:
            artwork = get_object_or_404(
                self.request.user.artist.artworks,
                id=artwork_id
            )
            kwargs['instance'] = artwork
        else:
            kwargs['instance'] = None
        return kwargs

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


class AddArtworkModalView(StaffRequiredMixin, FormView):
    template_name = 'dashboard/includes/add_artwork_modal.html'
    form_class = ArtworkSubmissionForm

    def form_valid(self, form):
        form.save(artist=self.request.user.artist)
        return JsonResponse({
            'success': True,
            'message': 'Artwork added successfully.'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        public_id = self.kwargs.get('public_id')
        if str(self.request.user.public_id) != public_id:
            return HttpResponseForbidden(
                "You are not authorized to view this page."
                )

        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['access'] = {
            'artwork_submissions': True,
            'artwork_removal': user.groups.filter(
                name__in=['Owner', 'Manager']
            ).exists(),
        }

        # Add context for artwork management functionality
        context['artwork_submission_form'] = ArtworkSubmissionForm()
        context['artwork_submissions'] = Artwork.objects.filter(
            is_available=False
        )
        return context
