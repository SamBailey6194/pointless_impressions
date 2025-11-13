from django import forms


# Add your forms here
class CartItemUpdateForm(forms.Form):
    """
    Form for updating cart item framing and quantity in checkout/order summary
    Dynamically sets framing_option choices based on artwork
    """

    quantity = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=99,
        widget=forms.NumberInput(attrs={
            'class': 'custom-input w-16 text-center',
            'min': '1',
            'max': '99',
        }),
        error_messages={
            'required': 'Quantity is required',
            'min_value': 'Quantity must be at least 1',
            'max_value': 'Quantity cannot exceed 99',
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
        super().__init__(*args, **kwargs)
        if artwork is not None:
            # Get all valid framing options for this artwork
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
