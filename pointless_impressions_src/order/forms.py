from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div, HTML


# Write your crispy form here
class OrderForm(forms.Form):
    """
    Form for collecting customer details during checkout.
    """
    email = forms.EmailField(
        required=True,
        label="Email Address",
        help_text="We'll send your order confirmation here.",
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )

    phone = forms.CharField(
        required=True,
        label="Phone Number",
        help_text="Enter your contact phone number.",
        widget=forms.TextInput(attrs={'placeholder': '+1234567890'})
    )

    shipping_name_addressee = forms.CharField(label="Full Name")
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
    shipping_country = forms.CharField(label="Country")

    billing_same_as_shipping = forms.BooleanField(
        required=False,
        label="Billing address same as shipping",
        initial=False,
        help_text=(
            "Check if your billing address is the "
            "same as your shipping address."
            )
    )

    billing_name_addressee = forms.CharField(label="Full Name")
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
    billing_country = forms.CharField(label="Country")

    def __init__(self, *args, **kwargs):
        """
        Add Crispy Form helper and hide email field for logged-in users.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.form_action = reverse('order:confirmation')

        self.helper.form_tag = True

        self.helper.layout = Layout(
            HTML(
                "<h3 class='text-lg font-semibold mb-4'>"
                "Contact Information"
                "</h3>"
                ),
            Div(
                Field('email', css_class='w-full lg:w-1/2 mb-4'),
                Field('phone', css_class='w-full lg:w-1/2 mb-4'),
                css_class='contact-group lg:flex lg:gap-4 mb-4'
            ),

            HTML(
                "<h3 class='text-lg font-semibold mb-4'>Shipping Address</h3>"
                ),
            Div(
                Div(id="saved-shipping-address-container", css_class="mb-4"),
                Field('shipping_name_addressee', css_class='mb-4'),
                Field('shipping_address_line_1', css_class='mb-4'),
                Field('shipping_address_line_2', css_class='mb-4'),
                Div(
                    Field('shipping_city', css_class='w-full lg:w-1/2'),
                    Field('shipping_county', css_class='w-full lg:w-1/2'),
                    css_class='lg:flex lg:gap-4 mb-4'
                ),
                Div(
                    Field('shipping_postcode', css_class='w-full lg:w-1/2'),
                    Field('shipping_country', css_class='w-full lg:w-1/2'),
                    css_class='lg:flex lg:gap-4 mb-4'
                ),
                css_class='shipping-group'
            ),

            Field('billing_same_as_shipping', css_class='mb-4'),

            Div(
                HTML(
                    "<h3 class='text-xl font-semibold mb-2'>"
                    "Billing Address"
                    "</h3>"
                    ),
                Div(
                    HTML(
                        "<p class='mb-4'>"
                        "Same as shipping address"
                        "</p>"
                    ),
                    HTML(
                        "<p class='mb-4' id='billing-confirmation-text'></p>"
                    ),
                    css_class='billing-confirmation-container mb-4',
                    style="display: none;"
                ),
                Div(id="saved-billing-address-container", css_class="mb-4"),
                Field('billing_name_addressee', css_class='mb-4'),
                Field('billing_address_line_1', css_class='mb-4'),
                Field('billing_address_line_2', css_class='mb-4'),
                Div(
                    Field('billing_city', css_class='w-full lg:w-1/2'),
                    Field('billing_county', css_class='w-full lg:w-1/2'),
                    css_class='lg:flex lg:gap-4 mb-4'
                ),
                Div(
                    Field('billing_postcode', css_class='w-full lg:w-1/2'),
                    Field('billing_country', css_class='w-full lg:w-1/2'),
                    css_class='lg:flex lg:gap-4 mb-4'
                ),
                css_class='billing-group'
            ),

            Submit(
                'submit',
                'Place Your Order',
                css_class='btn btn-ghost btn-outline btn-md mt-4'
                )
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

        if not billing_same:
            required_billing_fields = [
                'billing_name_addressee',
                'billing_address_line_1',
                'billing_city',
                'billing_postcode',
                'billing_country'
            ]

            for field_name in required_billing_fields:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, 'This field is required.')

        return cleaned_data
