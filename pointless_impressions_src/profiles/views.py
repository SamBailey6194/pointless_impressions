from django.views.generic import FormView, View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import logging
from .models import UserProfile, Customer
from .forms import (
    SignupForm,
    LoginForm,
    EmailVerificationForm,
    AddressForm,
    LogoutForm
)
from .mixins import CustomerRequiredMixin
from pointless_impressions_src.photo.forms import ProfilePhotoForm
from pointless_impressions_src.account.models import (
    EmailVerificationCode, CustomUser
    )
from pointless_impressions_src.account.mixins import (
    AnonymousRequiredMixin, EmailNotVerifiedMixin
    )
from pointless_impressions_src.account.utils import (
    send_verification_email, generate_verification_code,
    send_email_verified_confirmation
)

logger = logging.getLogger(__name__)


# Create your views here
class SignupView(View, AnonymousRequiredMixin):
    """
    User signup view that handles user registration and login upon successful
    signup.

    GET request renders the signup, profile pic, and address forms.

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
    template_name = 'profiles/signup.html'

    def get(self, request, *args, **kwargs):
        context = {
            'signup_form': SignupForm(),
            'profile_pic_form': ProfilePhotoForm(),
            # prefix='addr' prevents field name collisions (first_name/last_name
            # appear in both SignupForm and AddressForm). auto_id prevents
            # duplicate HTML IDs. Both are required together.
            'address_form': AddressForm(prefix='addr', auto_id='addr_%s'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        signup_form = SignupForm(request.POST)
        profile_pic_form = ProfilePhotoForm(
            request.POST, request.FILES
        )
        # prefix='addr' + auto_id prevents field name and HTML ID collisions
        # with SignupForm — see get() for context.
        address_form = AddressForm(request.POST, prefix='addr', auto_id='addr_%s')

        try:
            return self._process_signup(
                request, signup_form, profile_pic_form, address_form
            )
        except Exception:
            logger.exception("Unhandled exception in SignupView.post()")
            raise

    def _process_signup(self, request, signup_form, profile_pic_form, address_form):
        if (
            signup_form.is_valid() and
            profile_pic_form.is_valid() and
            address_form.is_valid()
        ):
            with transaction.atomic():
                user = signup_form.save(commit=False)
                user.is_active = False
                user.save()

                request.session['pending_verification_user_id'] = user.id

                user_profile = UserProfile.objects.create(user=user)
                customer = Customer.objects.create(
                    user_profile=user_profile
                )

                verification_code = generate_verification_code(user)

                photo = profile_pic_form.save(
                    commit=False,
                    user=user,
                    user_profile=user_profile
                )
                if photo:
                    photo.save()

                    if user_profile:
                        user_profile.profile_picture = photo
                        user_profile.save()

                address = address_form.save(commit=False)
                address.customer = customer
                address.save()

            try:
                send_verification_email(user)
            except Exception:
                logger.exception(
                    "Failed to send verification email to user %s", user.id
                )
                messages.warning(
                    request,
                    "Account created but we could not send your verification "
                    "email. Please use 'Resend code'."
                )

            messages.success(
                request, "Signup successful! Please verify your email."
            )
            return redirect('profiles:verify_email')
        else:
            messages.error(request, "Please correct the errors below.")
            context = {
                'signup_form': signup_form,
                'profile_pic_form': profile_pic_form,
                'address_form': address_form,
            }
            return render(request, self.template_name, context)


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
    template_name = 'profiles/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(self.request, user)
            messages.success(self.request, "Login successful!")
            return redirect('dashboard:landing')
        messages.error(self.request, "Invalid username or password.")
        return self.form_invalid(form)


class LogoutView(
    FormView,
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
    template_name = 'profiles/logout.html'
    form_class = LogoutForm

    def form_valid(self, form):
        logout(self.request)
        messages.success(self.request, "You have been logged out.")
        return redirect('home')


class VerifyEmailView(FormView):
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

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get('pending_verification_user_id')
        if not user_id:
            messages.error(
                request, "No pending verification found. Please sign up."
            )
            return redirect('profiles:signup')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        code = form.cleaned_data['verification_code']
        user_id = self.request.session.get('pending_verification_user_id')
        try:
            user = CustomUser.objects.get(id=user_id)
            verification = EmailVerificationCode.objects.get(
                code=code, is_used=False
            )
            if verification.is_expired():
                messages.error(self.request, "Verification code has expired.")
                return self.form_invalid(form)

            # Mark the verification code as used
            verification.is_used = True
            verification.save()

            # Activate the user
            user.is_active = True
            user.save()

            # Send email verified confirmation
            send_email_verified_confirmation(user)

            # Log the user in now they are verified and active
            login(self.request, user)

            messages.success(self.request, "Your email has been verified!")
            return redirect('dashboard:landing')

        except CustomUser.DoesNotExist:
            messages.error(self.request, "User not found.")
            return self.form_invalid(form)
        except EmailVerificationCode.DoesNotExist:
            messages.error(self.request, "Invalid verification code.")
            return self.form_invalid(form)


class ResendVerificationCodeView(View):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('pending_verification_user_id')

        if not user_id:
            return JsonResponse({
                "success": False,
                "message": "No pending verification found."
            }, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
            # Generate a new verification code
            generate_verification_code(user)

            # Use the utility function to send the email
            send_verification_email(user)

            return JsonResponse({
                "success": True,
                "message": "Verification code resent successfully."
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "User not found."
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "success": False, "message": str(e)
                }, status=500)
