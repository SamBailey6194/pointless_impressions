from django import forms
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Div, Submit
from pointless_impressions_src.order.models import OrderItem
from pointless_impressions_src.home.widgets import CountrySelectFormWidget
from pointless_impressions_src.home.countries import COUNTRY_CHOICES
from pointless_impressions_src.order.models import Order


class EditOrderForm(forms.Form):
    items = forms.ModelMultipleChoiceField(
        queryset=OrderItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select items to modify"
    )
    quantities = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Quantity",
        widget=forms.NumberInput(
            attrs={
                'class': 'text-center custom-input !w-24',
                'id': 'id_quantity'
            }
        )
    )
    framing_option = forms.ChoiceField(
        choices=[],
        required=False,
        label="Framing Options",
        widget=forms.Select(
            attrs={
                'class': 'select-dropdown w-full',
                'id': 'id_framing_option'
            }
        )
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Enter notes as a JSON object, e.g., {"item_id": "new_note"}'
            ),
            'rows': 3,
            'class': 'custom-input'
        }),
        required=False,
        label="Notes"
    )
    shipping_first_name = forms.CharField(
        max_length=255,
        required=False,
        label="Shipping First Name"
    )
    shipping_last_name = forms.CharField(
        max_length=255,
        required=False,
        label="Shipping Last Name"
    )
    shipping_address_line_1 = forms.CharField(
        max_length=255,
        required=False,
        label="Shipping Address Line 1"
    )
    shipping_address_line_2 = forms.CharField(
        max_length=255,
        required=False,
        label="Shipping Address Line 2"
    )
    shipping_city = forms.CharField(
        max_length=255,
        required=False,
        label="Shipping City"
    )
    shipping_county = forms.CharField(
        max_length=255,
        required=False,
        label="Shipping County"
    )
    shipping_postcode = forms.CharField(
        max_length=20,
        required=False,
        label="Shipping Postcode"
    )
    shipping_country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=False,
        label="Shipping Country",
        widget=CountrySelectFormWidget(
            attrs={
                'class': 'custom-input w-full lg:w-66'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        artwork = kwargs.pop('artwork', None)
        super().__init__(*args, **kwargs)

        if artwork:
            # Populate framing options dynamically
            self.fields['framing_option'].choices = [
                (condition.id, condition.condition_friendly_name)
                for condition in artwork.selected_conditions.all()
            ]

            max_stock = artwork.stock
            self.fields['quantities'].widget.attrs['max'] = max_stock

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 class='card-title text-center mb-4 "
                    "text-(--pointless-black) "
                    "dark:text-(--pointless-white)'>Edit Order</h2>"
                ),
                Div(
                    HTML(
                        """
                        <label for="id_quantity" class="font-bold text-lg \
                        text-(--pointless-black) \
                        dark:text-(--pointless-white)">
                        Quantity
                        </label>
                        <div class="flex items-center space-x-2">
                            <button type="button" class="btn btn-outline" \
                            id="decrement-quantity">-</button>
                            <input type="number" name="quantity" \
                                   id="id_quantity" \
                                   class="text-center custom-input !w-24" \
                                   value="1" min="1">
                            <button type="button" class="btn btn-outline" \
                            id="increment-quantity">+</button>
                        </div>
                        """
                    ),
                    Field(
                        'framing_option',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'notes',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_first_name',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_last_name',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_address_line_1',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_address_line_2',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_city',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_county',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_postcode',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    Field(
                        'shipping_country',
                        css_class='mb-4 custom-input w-full lg:w-66'
                    ),
                    css_class='flex flex-col gap-4'
                ),
                Div(
                    Submit(
                        'submit',
                        'Save Changes',
                        css_class='btn btn-ghost btn-outline w-fit'
                    ),
                    css_class='flex justify-end mt-4'
                ),
                css_class='px-6 py-2 mb-4',
                id='edit-order-form'
            )
        )

    def save(self, order_id):
        order = Order.objects.get(id=order_id)
        data = self.cleaned_data

        # Update quantities
        if data['quantities']:
            quantities = json.loads(data['quantities'])
            for item_id, quantity in quantities.items():
                item = order.items.get(id=item_id)
                item.quantity = quantity
                item.save()

        # Update framing options
        if data['framing_options']:
            framing_options = json.loads(data['framing_options'])
            for item_id, framing_option in framing_options.items():
                item = order.items.get(id=item_id)
                item.framing_condition = framing_option
                item.save()

        # Update notes
        if data['notes']:
            notes = json.loads(data['notes'])
            for item_id, note in notes.items():
                item = order.items.get(id=item_id)
                item.notes = note
                item.save()

        # Remove items
        if data['items']:
            for item in data['items']:
                order.items.remove(item)

        # Update shipping details
        order.shipping_first_name = data.get(
            'shipping_first_name', order.shipping_first_name
        )
        order.shipping_last_name = data.get(
            'shipping_last_name', order.shipping_last_name
        )
        order.shipping_address_line_1 = data.get(
            'shipping_address_line_1', order.shipping_address_line_1
        )
        order.shipping_address_line_2 = data.get(
            'shipping_address_line_2', order.shipping_address_line_2
        )
        order.shipping_city = data.get(
            'shipping_city', order.shipping_city
        )
        order.shipping_county = data.get(
            'shipping_county', order.shipping_county
        )
        order.shipping_postcode = data.get(
            'shipping_postcode', order.shipping_postcode
        )
        order.shipping_country = data.get(
            'shipping_country', order.shipping_country
        )

        order.save()
