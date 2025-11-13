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
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            })
    )

    phone = forms.CharField(
        required=True,
        label="Phone Number",
        help_text="Enter your contact phone number.",
        widget=forms.TextInput(attrs={
            'placeholder': '+1234567890',
            })
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
        self.helper.form_action = reverse('orders:confirmation')
        self.helper.form_tag = True

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
                            css_class='custom-input w-full lg:w-66'
                            ),
                        css_class='lg:flex lg:gap-4 mb-2'
                    ),

                    HTML(
                        "<div class='form-divider'></div>"
                        ),

                    HTML("<h3 class='card-title mb-2'>Shipping Address</h3>"),
                    Div(
                        Div(
                            HTML("<p>Enter your shipping details below</p>"),
                            id="saved-shipping-address-container"
                            ),
                        Field(
                            'shipping_name_addressee',
                            placeholder="Full Name",
                            css_class='mb-4 custom-input w-full'
                        ),
                        Field(
                            'shipping_address_line_1',
                            placeholder="Address Line 1",
                            css_class='mb-4 custom-input w-full'
                        ),
                        Field(
                            'shipping_address_line_2',
                            placeholder="Address Line 2 (Optional)",
                            css_class='mb-4 custom-input w-full'
                        ),
                        Div(
                            Field(
                                'shipping_city',
                                placeholder="City/Town",
                                css_class='w-full lg:w-1/2 custom-input'
                            ),
                            Field(
                                'shipping_county',
                                placeholder="County (Optional)",
                                css_class='w-full lg:w-1/2 custom-input'
                            ),
                            css_class='lg:flex lg:gap-4 mb-4'
                        ),
                        Div(
                            Field(
                                'shipping_postcode',
                                placeholder="Postcode",
                                css_class='w-full lg:w-1/2 custom-input'
                            ),
                            Field(
                                'shipping_country',
                                placeholder="Country",
                                css_class='w-full lg:w-1/2 custom-input'
                            ),
                            css_class='lg:flex lg:gap-4 mb-4'
                        ),
                        css_class='shipping-group'
                    ),

                    HTML("<div class='form-divider'></div>"),

                    HTML(
                        "<h3 class='card-title mb-2'>Billing Address</h3>"
                        "<p>Enter your billing details below</p>"
                        ),

                    Field(
                        'billing_same_as_shipping',
                        css_class='mr-4'
                        ),

                    Div(
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
                                'billing-confirmation-container'
                                'p-3 rounded-lg'
                                'mb-4'
                                ),
                            style="display: none;"
                        ),

                        Div(
                            Div(
                                id="saved-billing-address-container",
                                css_class="mb-4"
                                ),
                            Field(
                                'billing_name_addressee',
                                placeholder="Full Name",
                                css_class='mb-4 custom-input w-full'
                            ),
                            Field(
                                'billing_address_line_1',
                                placeholder="Address Line 1",
                                css_class='mb-4 custom-input w-full'
                            ),
                            Field(
                                'billing_address_line_2',
                                placeholder="Address Line 2 (Optional)",
                                css_class='mb-4 custom-input w-full'
                            ),
                            Div(
                                Field(
                                    'billing_city',
                                    placeholder="City/Town",
                                    css_class='w-full lg:w-1/2 custom-input'
                                ),
                                Field(
                                    'billing_county',
                                    placeholder="County (Optional)",
                                    css_class='w-full lg:w-1/2 custom-input'
                                ),
                                css_class='lg:flex lg:gap-4 mb-4'
                            ),
                            Div(
                                Field(
                                    'billing_postcode',
                                    placeholder="Postcode",
                                    css_class='w-full lg:w-1/2 custom-input'
                                ),
                                Field(
                                    'billing_country',
                                    placeholder="Country",
                                    css_class='w-full lg:w-1/2 custom-input'
                                ),
                                css_class='lg:flex lg:gap-4 mb-4'
                            ),
                        ),
                        css_class='billing-group',
                        id="billing-fields-container",
                    ),

                    HTML("<div class='form-divider'></div>"),

                    Submit(
                        'submit',
                        'Place Your Order',
                        css_class='btn btn-primary w-fit mt-4'
                    ),
                    css_class="card-body"
                ),
                css_class="card checkout-card"
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
