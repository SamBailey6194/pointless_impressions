from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Div
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
        self.fields['first_name'].label = "Your First Name"
        self.fields['last_name'].label = "Your Last Name"
        self.fields['username'].label = "Choose a Username"
        self.fields['phone'] = SplitPhoneNumberField(
            required=True,
            label="Phone Number",
            region='GB',
        )
        self.fields['email'].label = "Email Address"
        self.fields['password1'] = forms.CharField(
            label="Create a Password",
            widget=forms.PasswordInput,
            validators=[CustomPasswordValidator]
        )
        self.fields['password2'] = forms.CharField(
            label="Confirm Your Password",
            widget=forms.PasswordInput,
            validators=[CustomPasswordValidator]
        )
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                HTML("<h2 class='card-title text-center'>Sign Up</h2>"),
                Div(
                    Div(
                        HTML("<h4 class='mb-2'>Name</h4>"),
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
                    Div(
                        HTML("<h4 class='mb-2'>User Information</h4>"),
                        Field(
                            'username',
                            placeholder="Username",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'phone',
                            placeholder="Phone Number",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'email',
                            placeholder="Email",
                            css_class='mb-4 custom-input w-full lg:w-1/2'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    Div(
                        HTML("<h4 class='mb-2'>Password</h4>"),
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
                            "<p class='text-sm text-gray-500'>"
                            "By signing up, you agree to our terms.</p>"
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    Submit(
                        'submit',
                        'Sign Up',
                        css_class='btn btn-ghost btn-outline w-fit'
                        ),
                    css_class='flex flex-col card-body gap-4'
                ),
                css_class='card p-6 mb-6'
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
                HTML("<h2 class='card-title text-center'>Log In</h2>"),
                Div(
                    Field(
                        'username',
                        placeholder="Username",
                        css_class='mb-4 custom-input w-full lg:w-66'
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
                    css_class='flex flex-col card-body gap-4'
                ),
                css_class='card p-6 mb-6'
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
                HTML("<h2 class='card-title text-center'>Log Out</h2>"),
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
                    css_class='flex flex-col card-body gap-4'
                ),
                css_class='card p-6 mb-6'
            )
        )


class ArtistApplicationForm(forms.ModelForm):
    """Form for artist application."""
    class Meta:
        model = Artist
        fields = ['bio', 'portfolio_url', 'social_links']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['bio'].label = "Artist Biography"
        self.fields['portfolio_url'].label = "Portfolio URL"
        self.fields['social_links'].label = "Social Media Links"
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 class='card-title text-center'>"
                    "Artist Application</h2>"
                    ),
                Div(
                    Field(
                        'bio',
                        placeholder="Tell us about yourself as an artist"
                        ),
                    Field(
                        'portfolio_url',
                        placeholder="Link to your portfolio"
                        ),
                    Div(
                        Field('social_links', css_class='social-links'),
                        HTML(
                            "<button"
                            "type='button'"
                            "class='btn btn-secondary add-social'>"
                            "Add Social</button>"
                        ),
                        css_class='social-links-container'
                    ),
                    Submit(
                        'submit',
                        'Apply',
                        css_class='btn btn-primary w-fit'
                        ),
                    css_class='flex flex-col card-body gap-4'
                ),
                css_class='flex flex-col card gap-4'
            )
        )

    def clean_social_links(self):
        """Validate social links as URLs."""
        social_links = self.data.getlist('social_links')
        for url in social_links:
            if not url:
                continue
            try:
                forms.URLField().clean(url)
            except forms.ValidationError:
                raise forms.ValidationError(f"Invalid URL: {url}")
        return social_links

    def save(self, commit=True):
        artist = super().save(commit=False)
        if self.user:
            artist.user_profile = self.user.user_profile
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
            'address_line1',
            'address_line2',
            'city',
            'state',
            'zip_code',
            'country',
            'is_default'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address_type'].widget = forms.Select(choices=[
            ('SHIPPING', 'Shipping'),
            ('BILLING', 'Billing')
        ])
        self.fields['is_default'].widget = forms.CheckboxInput()
        self.fields['country'] = forms.ChoiceField(
            choices=COUNTRY_CHOICES,
            initial='GB',
            label="Country",
            widget=CountrySelectFormWidget()
        )
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h3 class='card-title mb-2'>"
                    "Address</h3>"
                ),
                Div(
                    HTML(
                        "<p class='mb-4'>"
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
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    Div(
                        HTML("<h4 class='mb-2'>Recipient Name</h4>"),
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
                            'address_line1',
                            placeholder="Address Line 1",
                            css_class='mb-4 custom-input w-full lg:w-96'
                        ),
                        Field(
                            'address_line2',
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
                            'post_code',
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
                    Submit(
                        'submit',
                        'Save Address',
                        css_class='btn btn-ghost btn-outline w-fit'
                    ),
                    css_class='flex flex-col card-body gap-4'
                ),
                css_class='card p-6 mb-6'
            )
        )
