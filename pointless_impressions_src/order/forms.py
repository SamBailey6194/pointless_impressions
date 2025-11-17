from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML
from phonenumber_field.formfields import SplitPhoneNumberField
from pointless_impressions_src.home.widgets import CountrySelectFormWidget
from pointless_impressions_src.home.countries import COUNTRY_CHOICES


# Write your crispy form here
class OrderForm(forms.Form):
    """
    Form for collecting customer details during checkout.

    Authenticated users:
    - Email and phone fields are hidden.
    - Addresses are a dropdown of saved addressed in DB.
    - Shipping and billing addresses can be the same or different.

    Guest Users:
    - Must fill in all fields manually.
    - Shipping and billing addresses can be the same or different.

    Fields:
    - email: Customer's email address.
    - phone: Customer's phone number.
    - shipping_first_name: Full name for shipping.
    - shipping_last_name: Full name for shipping.
    - shipping_address_line_1: Shipping address line 1.
    - shipping_address_line_2: Shipping address line 2 (optional).
    - shipping_city: Shipping city/town.
    - shipping_county: Shipping county (optional).
    - shipping_postcode: Shipping postcode.
    - shipping_country: Shipping country.
    - billing_same_as_shipping: Checkbox if billing address is same as
      shipping.
    - billing_first_name: Full name for billing.
    - billing_last_name: Full name for billing.
    - billing_address_line_1: Billing address line 1.
    - billing_address_line_2: Billing address line 2 (optional).
    - billing_city: Billing city/town.
    - billing_county: Billing county (optional).
    - billing_postcode: Billing postcode.
    - billing_country: Billing country.

    If the user address is outside UK, they will be asked to email the order
    number to our support team for manual processing, as payments on the
    website are not supported for international addresses at this time.
    """
    email = forms.EmailField(
        required=True,
        label="Email Address",
        help_text="We'll send your order confirmation here.",
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            })
    )

    phone = SplitPhoneNumberField(
        required=True,
        label="Phone Number",
        region='GB',
    )

    shipping_first_name = forms.CharField(label="First Name")
    shipping_last_name = forms.CharField(label="Last Name")
    shipping_address_line_1 = forms.CharField(label="Address Line 1")
    shipping_address_line_2 = forms.CharField(
        label="Address Line 2 (Optional)",
        required=False
    )
    shipping_city = forms.CharField(label="City/Town")
    shipping_county = forms.CharField(
        label="County (Optional)",
        required=False
    )
    shipping_postcode = forms.CharField(label="Postcode")
    shipping_country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        initial='GB',
        label="Country",
        widget=CountrySelectFormWidget()
    )

    billing_same_as_shipping = forms.BooleanField(
        required=False,
        label="Billing address same as shipping",
        initial=False,
        help_text=(
            "Check if your billing address is the "
            "same as your shipping address."
            )
    )

    billing_first_name = forms.CharField(label="First Name")
    billing_last_name = forms.CharField(label="Last Name")
    billing_address_line_1 = forms.CharField(label="Address Line 1")
    billing_address_line_2 = forms.CharField(
        label="Address Line 2 (Optional)",
        required=False
        )
    billing_city = forms.CharField(label="City/Town")
    billing_county = forms.CharField(
        label="County (Optional)",
        required=False
        )
    billing_postcode = forms.CharField(label="Postcode")
    billing_country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        initial='GB',
        label="Country",
        widget=CountrySelectFormWidget()
    )

    def __init__(self, *args, **kwargs):
        """
        Add Crispy Form helper and hide email field for logged-in users.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        "<h3 class='card-title mb-2'>Contact Information</h3>"
                    ),
                    Div(
                        Field(
                            'email',
                            css_class='custom-input w-full lg:w-66'
                        ),
                        Field(
                            'phone',
                            css_class=(
                                'custom-input '
                                'h-10 '
                                'w-full '
                                'lg:w-66 '
                                'my-2 '
                                'lg:my-0 '
                                'lg:mx-2 '
                                'rounded-lg'
                            )
                        ),
                        css_class='lg:flex lg:gap-4 mb-2'
                    ),

                    HTML(
                        "<div class='form-divider'></div>"
                    ),

                    Div(
                        HTML(
                            "<h3 class='card-title mb-2'>"
                            "Shipping Address</h3>"
                        ),
                        HTML(
                            "<p class='mb-4'>"
                            "Enter your shipping details below</p>"
                            ),
                        Div(
                            Field(
                                'shipping_first_name',
                                placeholder="First Name",
                                css_class='mb-4 custom-input w-full lg:w-66'
                            ),
                            Field(
                                'shipping_last_name',
                                placeholder="Last Name",
                                css_class='mb-4 custom-input w-full lg:w-66'
                            ),
                            css_class='lg:flex lg:gap-4 mb-4'
                        ),
                        Div(
                            Field(
                                'shipping_address_line_1',
                                placeholder="Address Line 1",
                                css_class='mb-4 custom-input w-full lg:w-96'
                            ),
                            Field(
                                'shipping_address_line_2',
                                placeholder="Address Line 2 (Optional)",
                                css_class='mb-4 custom-input w-full lg:w-96'
                            ),
                            css_class='mb-4 lg:flex lg:gap-4'
                        ),
                        Div(
                            Field(
                                'shipping_city',
                                placeholder="City/Town",
                                css_class='w-full lg:w-64 custom-input'
                            ),
                            Field(
                                'shipping_county',
                                placeholder="County (Optional)",
                                css_class='w-full lg:w-64 custom-input'
                            ),
                            css_class='lg:flex lg:gap-4 mb-4'
                        ),
                        Div(
                            Field(
                                'shipping_postcode',
                                placeholder="Postcode",
                                css_class='w-full lg:w-40 custom-input'
                            ),
                            Field(
                                'shipping_country'
                            ),
                            css_class='lg:flex lg:gap-4 mb-4'
                        ),
                        Field(
                            'billing_same_as_shipping',
                            css_class='mr-4'
                        ),
                        css_class='shipping-group',
                        id="shipping-fields-container",
                    ),

                    HTML("<div class='form-divider'></div>"),

                    Div(
                        HTML(
                            "<h3 class='card-title mb-2'>Billing Address</h3>"
                            "<p class='mb-4'>"
                            "Enter your billing details below"
                            "</p>"
                        ),
                        Div(
                            HTML(
                                "<p class='text-sm text-gray-600'>"
                                "Same as shipping address:"
                                "</p>"
                            ),
                            HTML(
                                "<p "
                                "class='font-semibold' "
                                "id='billing-confirmation-text'>"
                                "</p>"
                            ),
                            css_class=(
                                'billing-confirmation-container '
                                'p-3 rounded-lg '
                                'mb-4'
                            ),
                            style="display: none;"
                        ),
                        Div(
                            Div(
                                Field(
                                    'billing_first_name',
                                    placeholder="First Name",
                                    css_class=(
                                        'mb-4 custom-input w-full lg:w-66'
                                        )
                                ),
                                Field(
                                    'billing_last_name',
                                    placeholder="Last Name",
                                    css_class=(
                                        'mb-4 custom-input w-full lg:w-66'
                                        )
                                ),
                                css_class='lg:flex lg:gap-4 mb-4'
                            ),
                            Div(
                                Field(
                                    'billing_address_line_1',
                                    placeholder="Address Line 1",
                                    css_class=(
                                        'mb-4 custom-input w-full lg:w-96'
                                        )
                                ),
                                Field(
                                    'billing_address_line_2',
                                    placeholder="Address Line 2 (Optional)",
                                    css_class=(
                                        'mb-4 custom-input w-full lg:w-96'
                                        )
                                ),
                                css_class='mb-4 lg:flex lg:gap-4'
                            ),
                            Div(
                                Field(
                                    'billing_city',
                                    placeholder="City/Town",
                                    css_class='w-full lg:w-64 custom-input'
                                ),
                                Field(
                                    'billing_county',
                                    placeholder="County (Optional)",
                                    css_class='w-full lg:w-64 custom-input'
                                ),
                                css_class='lg:flex lg:gap-4 mb-4'
                            ),
                            Div(
                                Field(
                                    'billing_postcode',
                                    placeholder="Postcode",
                                    css_class='w-full lg:w-40 custom-input'
                                ),
                                Field(
                                    'billing_country'
                                ),
                                css_class='lg:flex lg:gap-4 mb-4'
                            ),
                        ),
                        css_class='billing-group',
                        id="billing-fields-container",
                    ),

                    HTML("<div class='form-divider'></div>"),
                ),
                css_class='card-body p-6'
            ),
        )

        if user and user.is_authenticated:
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['email'].label = False
            self.fields['email'].help_text = False
            self.fields['phone'].widget = forms.HiddenInput()
            self.fields['phone'].label = False
            self.fields['phone'].help_text = False

    def clean(self):
        """
        Ensure billing address is provided if not same as shipping.
        """
        cleaned_data = super().clean()
        billing_same = cleaned_data.get('billing_same_as_shipping')

        if billing_same:
            cleaned_data['billing_first_name'] = cleaned_data.get(
                'shipping_first_name'
                )
            cleaned_data['billing_last_name'] = cleaned_data.get(
                'shipping_last_name'
                )
            cleaned_data['billing_address_line_1'] = cleaned_data.get(
                'shipping_address_line_1'
                )
            cleaned_data['billing_address_line_2'] = cleaned_data.get(
                'shipping_address_line_2'
                )
            cleaned_data['billing_city'] = cleaned_data.get(
                'shipping_city'
                )
            cleaned_data['billing_county'] = cleaned_data.get(
                'shipping_county'
                )
            cleaned_data['billing_postcode'] = cleaned_data.get(
                'shipping_postcode'
                )
            cleaned_data['billing_country'] = cleaned_data.get(
                'shipping_country'
                )
        else:
            required_billing_fields = [
                'billing_first_name',
                'billing_last_name',
                'billing_address_line_1',
                'billing_city',
                'billing_postcode',
                'billing_country'
            ]

            for field_name in required_billing_fields:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, 'This field is required.')

        return cleaned_data
