from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Div, Button
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from phonenumber_field.formfields import SplitPhoneNumberField
from .models import Artist, Address, UserProfile
from pointless_impressions_src.account.models import CustomUser
from pointless_impressions_src.home.widgets import CountrySelectFormWidget
from pointless_impressions_src.home.countries import COUNTRY_CHOICES
from pointless_impressions_src.account.validators import (
    CustomPasswordValidator
    )


# Write your forms here.
class SignupForm(UserCreationForm):
    """Form for user signup."""
    subscribe_to_newsletter = forms.BooleanField(
        required=False,
        label="Subscribe to Newsletter",
        help_text="Check this box to receive our newsletter.",
        initial=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'password1',
            'password2'
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'] = SplitPhoneNumberField(
            required=True,
            label="Phone Number",
            region='GB',
        )
        self.fields['password1'] = forms.CharField(
            label="Password",
            widget=forms.PasswordInput,
            validators=[CustomPasswordValidator]
        )
        self.fields['password2'] = forms.CharField(
            label="Confirm Password",
            widget=forms.PasswordInput,
            validators=[CustomPasswordValidator]
        )
        self.fields['subscribe_to_newsletter'] = forms.BooleanField(
            required=False,
            label="Subscribe to Newsletter",
            initial=False
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 class='card-title text-center "
                    "mb-4 "
                    "text-(--pointless-black) "
                    "dark:text-(--pointless-white)'>Sign Up</h2>"
                ),
                Div(
                    HTML(
                        "<h4 class='mb-2 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>Name</h4>"
                    ),
                    Div(
                        Field(
                            'first_name',
                            placeholder="First Name",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'last_name',
                            placeholder="Last Name",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    HTML(
                        "<h4 class='mb-2 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>"
                        "User Information</h4>"
                    ),
                    Div(
                        Field(
                            'username',
                            placeholder="Username",
                            css_class='lg:mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'phone',
                            placeholder="0123456789",
                            css_class=(
                                'custom-input '
                                'h-10 '
                                'w-full '
                                'lg:w-66 '
                                'my-2 '
                                'lg:my-0 '
                                'lg:mr-4 '
                                'lg:mt-2'
                                'rounded-lg'
                            )
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    Div(
                        Field(
                            'email',
                            placeholder="Email",
                            css_class='mb-4 custom-input w-full'
                        ),
                        Field(
                            'subscribe_to_newsletter',
                            css_class='mb-4'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    HTML(
                        "<h4 class='mb-2 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>Password</h4>"
                    ),
                    Div(
                        Field(
                            'password1',
                            placeholder="Password",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'password2',
                            placeholder="Confirm Password",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    HTML(
                            "<p class='text-sm text-(--pointless-black) "
                            "dark:text-(--pointless-white)'>"
                            "By signing up, you agree to our terms.</p>"
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    css_class=(
                        'flex '
                        'flex-col '
                        'gap-4'
                        )
                ),
                css_class='px-6 py-2 mb-4',
                id='signup-form'
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    """Form for user login."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 "
                    "class="
                    "'card-title "
                    "text-center "
                    "text-(--pointless-black) "
                    "dark:text-(--pointless-white) "
                    "mb-4'>"
                    "Log In</h2>"
                    ),
                Div(
                    HTML(
                        "<label class='text-(--pointless-black) "
                        "dark:text-(--pointless-white) "
                        "mb-4'>"
                        "Username</label>"
                    ),
                    Field(
                        'username',
                        placeholder="Username",
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    HTML(
                        "<label class='text-(--pointless-black) "
                        "dark:text-(--pointless-white) "
                        "mb-4'>"
                        "Password</label>"
                    ),
                    Field(
                        'password',
                        placeholder="Password",
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Submit(
                        'submit',
                        'Log In',
                        css_class='btn btn-ghost btn-outline w-fit'
                    ),
                    css_class=(
                        'flex '
                        'flex-col '
                        'gap-4 '
                        'bg-gray-300 '
                        'dark:bg-gray-700 '
                        )
                ),
                css_class='p-6 mb-6 form-card',
                id='login-form'
            )
        )


class LogoutForm(forms.Form):
    """Form for user logout."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 "
                    "class="
                    "'card-title "
                    "text-center "
                    "text-(--pointless-black) "
                    "dark:text-(--pointless-white) "
                    "mb-4'>"
                    "Logout</h2>"
                ),
                Div(
                    HTML(
                        "<p class='mb-4'>"
                        "Are you sure you want to log out?</p>"
                    ),
                    Submit(
                        'submit',
                        'Log Out',
                        css_class='btn btn-ghost btn-outline w-fit'
                    ),
                    css_class=(
                        'flex '
                        'flex-col '
                        'gap-4 '
                        )
                ),
                css_class='p-6 mb-6 form-card',
                id='logout-form'
            )
        )


class ArtistApplicationForm(forms.ModelForm):
    """
    Form for artist application with split social_links field.
    """
    social_links = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Artist
        fields = ['bio', 'portfolio_url', 'social_links']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].label = "Artist Biography"
        self.fields['portfolio_url'].label = "Portfolio URL"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 class='card-title text-center "
                    "text-(--pointless-black) dark:text-(--pointless-white) "
                    "mb-4'>Artist Application</h2>"
                ),
                Div(
                    Field(
                        'bio',
                        css_class='mb-4 custom-input w-full',
                        placeholder="Tell us about yourself as an artist"
                    ),
                    Field(
                        'portfolio_url',
                        placeholder="Link to your portfolio",
                        css_class='mb-4 custom-input w-full'
                    ),
                    Div(
                        HTML(
                            "<h4 class='mb-2 text-(--pointless-black) "
                            "dark:text-(--pointless-white)'>Social Links</h4>"
                        ),
                        HTML(
                            "<div id='social-links-container'>"
                            "<div class='social-link-row flex gap-4 mb-4'>"
                            "<input type='text' name='platform' "
                            "class='custom-input w-1/3 rounded-lg' "
                            "placeholder='Platform'>"
                            "<input type='url' name='url' "
                            "class='custom-input w-2/3 rounded-lg' "
                            "placeholder='URL'>"
                            "<button type='button' "
                            "class='btn btn-ghost btn-outline remove-social'>"
                            "Remove</button>"
                            "</div>"
                            "</div>"
                        ),
                        HTML(
                            "<button type='button' id='add-social-link' "
                            "class='btn btn-ghost btn-outline'>"
                            "Add Social Link</button>"
                        ),
                        css_class='social-links-container'
                    ),
                    css_class='flex flex-col'
                ),
                css_class='flex flex-col p-4 mb-4',
                id='artist-application-form'
            )
        )

    def clean_social_links(self):
        """Validate and parse social links."""
        social_links = self.data.getlist('social_links')
        parsed_links = []
        for link in social_links:
            try:
                platform, url = link.split('|')
                forms.URLField().clean(url)
                parsed_links.append({'platform': platform, 'url': url})
            except (ValueError, forms.ValidationError):
                raise forms.ValidationError(f"Invalid social link: {link}")
        return parsed_links

    def save(self, commit=True):
        artist = super().save(commit=False)
        artist.social_links = self.cleaned_data['social_links']
        if commit:
            artist.save()
        return artist


class AddressForm(forms.ModelForm):
    """Form for user address."""
    class Meta:
        model = Address
        fields = [
            'label',
            'address_type',
            'first_name',
            'last_name',
            'address_line_1',
            'address_line_2',
            'city',
            'county',
            'postcode',
            'country',
            'is_default'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address_type'].widget = forms.CheckboxSelectMultiple(
            choices=[
                ('SHIPPING', 'Shipping'),
                ('BILLING', 'Billing')
            ]
        )
        self.fields['address_type'].help_text = "Select all that apply"
        self.fields['is_default'].widget = forms.CheckboxInput()
        self.fields['label'].label = "Address Label"
        self.fields['country'] = forms.ChoiceField(
            choices=COUNTRY_CHOICES,
            initial='GB',
            label="Country",
            widget=CountrySelectFormWidget()
        )
        self.fields['is_default'].label = "Set as Default Address"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 "
                    "class="
                    "'card-title "
                    "text-center "
                    "text-(--pointless-black) "
                    "dark:text-(--pointless-white) "
                    "mb-4'>"
                    "Address</h2>"
                ),
                Div(
                    HTML(
                        "<p class='text-(--pointless-black) "
                        "dark:text-(--pointless-white) "
                        "mb-4'>"
                        "Enter your address details below</p>"
                    ),
                    Div(
                        Field(
                            'label',
                            placeholder="Label (e.g., Home, Work)",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'address_type',
                            css_class='mb-4 w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<h4 class='text-(--pointless-black) "
                        "dark:text-(--pointless-white) "
                        "mb-4'>Recipient Name</h4>"
                    ),
                    Div(
                        Field(
                            'first_name',
                            placeholder="First Name",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'last_name',
                            placeholder="Last Name",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    Div(
                        Field(
                            'address_line_1',
                            placeholder="Address Line 1",
                            css_class='mb-4 custom-input w-full lg:w-96'
                        ),
                        Field(
                            'address_line_2',
                            placeholder="Address Line 2 (Optional)",
                            css_class='mb-4 custom-input w-full lg:w-96'
                        ),
                        css_class='mb-4 lg:flex lg:gap-4'
                    ),
                    Div(
                        Field(
                            'city',
                            placeholder="City/Town",
                            css_class='w-full lg:w-64 custom-input'
                        ),
                        Field(
                            'county',
                            placeholder="County (Optional)",
                            css_class='w-full lg:w-64 custom-input'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    Div(
                        Field(
                            'postcode',
                            placeholder="Postcode",
                            css_class='w-full lg:w-40 custom-input'
                        ),
                        Field(
                            'country'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    Field(
                        'is_default',
                        css_class='mb-4'
                    ),
                    css_class=(
                        'flex '
                        'flex-col '
                        'gap-4 '
                        )
                ),
                css_class='p-4 mb-4',
                id='address-form'
            )
        )


class EmailVerificationForm(forms.Form):
    """Form for email verification code input."""
    verification_code = forms.CharField(
        max_length=6,
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the 6-digit code',
                'class': 'custom-input w-full lg:w-40'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 "
                    "class="
                    "'card-title "
                    "text-center "
                    "text-(--pointless-black) "
                    "dark:text-(--pointless-white) "
                    "mb-4'>"
                    "Email Verification</h2>"
                    ),
                Div(
                    HTML(
                        "<p class='mb-4 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>"
                        "Please enter the 6-digit verification code "
                        "sent to your email.</p>"
                    ),
                    HTML(
                        "<label class='text-(--pointless-black) "
                        "dark:text-(--pointless-white) "
                        "mb-4'>"
                        "Verification Code</label>"
                    ),
                    Field(
                        'verification_code'
                    ),
                    HTML(
                        "<p class='text-(--pointless-black) "
                        "dark:text-(--pointless-white) "
                        "mb-4'>"
                        "If you didn't receive the code, click Resend Code."
                        "</p>"
                    ),
                    Div(
                        Submit(
                            'submit',
                            'Verify Email',
                            css_class='btn btn-ghost btn-outline w-fit'
                        ),
                        Button(
                            'resend',
                            'Resend Code',
                            css_class='btn btn-ghost btn-outline w-fit ml-2'
                        ),
                        css_class='flex items-center gap-2'
                    ),
                    css_class=(
                        'flex '
                        'flex-col '
                        'gap-4 '
                        )
                ),
                css_class='p-6 mb-6',
                id='email-verification-form'
            )
        )
