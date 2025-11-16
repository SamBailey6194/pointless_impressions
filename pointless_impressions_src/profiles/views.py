from django.views.generic import FormView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    SignupForm,
    LoginForm,
    EmailVerificationForm,
    ArtistApplicationForm,
    AddressForm,
    LogoutForm
)
from pointless_impressions_src.photo.forms import PhotoForm
from pointless_impressions_src.account.models import EmailVerificationCode
from pointless_impressions_src.account.mixins import (
    AnonymousRequiredMixin, EmailNotVerifiedMixin
    )


# Create your views here
class SignupView(FormView, AnonymousRequiredMixin):
    """
    User signup view that handles user registration and login upon successful
    signup.

    POST request with valid form data creates a new user, logs them in,
    and redirects to email verification page.

    Features:
    - Uses SignupForm to capture user details.
    - On successful form submission, creates a new user and logs them in.
    - Displays success message and redirects to 'verify_email' page.

    Template:
    - 'profiles/includes/signup_modal.html'

    Context:
    - form: Instance of SignupForm for user input.
    """
    template_name = 'profiles/includes/signup_modal.html'
    form_class = SignupForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo_form'] = PhotoForm(instance=self.request.user.profile)
        context['address_form'] = AddressForm(
            instance=self.request.user.profile
            )
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request, "Signup successful! Please verify your email."
        )
        return redirect('verify_email')


class LoginView(FormView, AnonymousRequiredMixin):
    """
    User login view that handles user login.

    POST request with valid form with data in the database
    and ensures it matches.

    Features:
    - Uses LoginForm to capture user details.
    - On successful form submission, authenticates and sends user an email.
    - Displays success message and redirects to 'email verification' page.

    Template:
    - 'profiles/includes/login_modal.html'

    Context:
    - form: Instance of LoginForm for user input.
    """
    template_name = 'profiles/includes/login_modal.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(self.request, user)
            messages.success(self.request, "Login successful!")
            return redirect('dashboard')
        messages.error(self.request, "Invalid username or password.")
        return self.form_invalid(form)


class LogoutView(
    View,
    LoginRequiredMixin
):
    """
    User logout view that handles user logout.

    GET request renders the logout confirmation modal.
    POST request logs out the user, displays a success message,
    and redirects to the home page.

    Features:
    - Renders a modal for logout confirmation.
    - Logs out the currently authenticated user upon confirmation.
    - Displays a success message upon logout.
    - Redirects to the 'home' page after logout.

    Template:
    - 'profiles/includes/logout_modal.html'

    Context:
    - N/A
    """
    template_name = 'profiles/includes/logout_modal.html'
    form_class = LogoutForm

    def form_valid(self, form):
        logout(self.request)
        messages.success(self.request, "You have been logged out.")
        return redirect('home')


class VerifyEmailView(FormView, EmailNotVerifiedMixin):
    """
    Email verification view that handles user email verification.

    POST request with valid verification code marks the user's email
    as verified.

    Features:
    - Uses EmailVerificationForm to capture verification code.
    - On successful form submission, verifies the code and activates the user.
    - Displays success or error messages based on verification outcome.

    Template:
    - 'profiles/verify_email.html'

    Context:
    - form: Instance of EmailVerificationForm for user input.
    """
    template_name = 'profiles/verify_email.html'
    form_class = EmailVerificationForm

    def form_valid(self, form):
        code = form.cleaned_data['verification_code']
        try:
            verification = EmailVerificationCode.objects.get(
                code=code, is_used=False
            )
            if verification.is_expired():
                messages.error(
                    self.request, "The verification code has expired."
                )
            else:
                verification.is_used = True
                verification.save()
                verification.user.is_active = True
                verification.user.save()
                messages.success(
                    self.request, "Your email has been verified successfully."
                )
                return redirect('dashboard')
        except EmailVerificationCode.DoesNotExist:
            messages.error(self.request, "Invalid verification code.")
        return self.form_invalid(form)


class ArtistApplicationView(FormView):
    """
    Artist application view that handles the submission of artist applications.

    Features:
    - Uses multiple forms: SignupForm, PhotoForm, AddressForm,
      and ArtistApplicationForm.
    - Handles both new user registration and existing user applications.
    - Displays success or error messages based on form submission outcome.

    Template:
    - 'profiles/templates/profiles/artist_application.html'

    Context:
    - signup_form: Instance of SignupForm for new user registration.
    - photo_form: Instance of PhotoForm for photo uploads.
    - address_form: Instance of AddressForm for address details.
    - artist_application_form: Instance of ArtistApplicationForm for
      artist-specific details.
    """
    template_name = 'profiles/templates/profiles/artist_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['artist_application_form'] = ArtistApplicationForm()
        else:
            context['signup_form'] = SignupForm()
            context['photo_form'] = PhotoForm()
            context['address_form'] = AddressForm()
            context['artist_application_form'] = ArtistApplicationForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            artist_application_form = ArtistApplicationForm(request.POST)

            if artist_application_form.is_valid():
                artist_application = artist_application_form.save(commit=False)
                artist_application.user = request.user
                artist_application.save()

                messages.success(
                    request, "Your artist application has been submitted."
                )
                return render(
                    request, self.template_name, self.get_context_data()
                    )

            messages.error(request, "Please correct the errors in the form.")
            return render(
                request,
                self.template_name,
                {'artist_application_form': artist_application_form},
            )
        else:
            signup_form = SignupForm(request.POST)
            photo_form = PhotoForm(request.POST, request.FILES)
            address_form = AddressForm(request.POST)
            artist_application_form = ArtistApplicationForm(request.POST)

            if (
                signup_form.is_valid()
                and photo_form.is_valid()
                and address_form.is_valid()
                and artist_application_form.is_valid()
            ):
                user = signup_form.save()
                photo = photo_form.save(commit=False)
                photo.user = user
                photo.save()

                address = address_form.save(commit=False)
                address.user = user
                address.save()

                artist_application = artist_application_form.save(commit=False)
                artist_application.user = user
                artist_application.save()

                messages.success(
                    request, "Your artist application has been submitted."
                )
                return render(
                    request, self.template_name, self.get_context_data()
                    )

            messages.error(request, "Please correct the errors in the form.")
            return render(
                request,
                self.template_name,
                {
                    'signup_form': signup_form,
                    'photo_form': photo_form,
                    'address_form': address_form,
                    'artist_application_form': artist_application_form,
                },
            )
