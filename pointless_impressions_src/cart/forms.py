from django import forms


# Add your forms here
class CartItemUpdateForm(forms.Form):
    """
    Form for updating cart item framing and quantity in checkout/order summary
    Dynamically sets framing_option choices based on artwork
    """

    quantity = forms.IntegerField(
        required=True,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'name': 'quantity',
            'class': 'custom-input w-16 text-center',
        }),
        error_messages={
            'max_value': 'Quantity cannot exceed item.quantity',
            'invalid': 'Please enter a valid quantity',
        }
    )

    framing_option = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(attrs={
            'class': (
                'custom-input w-32 md:w-48 js-framing-option text-[10px] '
                'md:text-sm'
                ),
        }),
        error_messages={'invalid_choice': 'Invalid framing option'}
    )

    def __init__(self, *args, **kwargs):
        artwork = kwargs.pop('artwork', None)
        max_quantity = kwargs.pop('max_quantity', 99)
        super().__init__(*args, **kwargs)

        if max_quantity:
            self.fields['quantity'].max_value = max_quantity
            self.fields['quantity'].widget.attrs['max'] = str(max_quantity)

        if artwork is not None:
            framing_qs = artwork.selected_conditions.all()
            if framing_qs.exists():
                choices = [
                    (str(f.id), f.condition_friendly_name)
                    for f in framing_qs.all()
                    ]
                self.fields['framing_option'].choices = choices
            else:
                self.fields['framing_option'].choices = [
                    ('', '— No Framing —')
                    ]
                self.fields['framing_option'].disabled = True
