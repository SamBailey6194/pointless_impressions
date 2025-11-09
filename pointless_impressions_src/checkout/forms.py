from django import forms
from django.core.exceptions import ValidationError
from pointless_impressions_src.artwork.models import (
    Artwork,
    ArtworkFramingCondition
)


# Add your forms here
class AddToCartForm(forms.Form):
    """
    Form for adding items to cart via modal
    Validates artwork ID, quantity, framing options, and notes
    """

    artwork_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput(),
        error_messages={'required': 'Artwork ID is required'}
    )

    quantity = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=999,
        widget=forms.NumberInput(
            attrs={
                'class': 'custom-input w-20 text-center',
                'id': 'quantity',
                'name': 'quantity',
                'min': '1',
                'max': '999',
            }
        ),
        error_messages={
            'required': 'Quantity is required',
            'min_value': 'Quantity must be at least 1',
            'max_value': 'Quantity cannot exceed 999',
            'invalid': 'Please enter a valid quantity',
        }
    )

    framing_option = forms.IntegerField(
        required=False,
        widget=forms.Select(
            choices=[],
            attrs={
                'class': 'custom-input w-full',
                'id': 'framing_option',
                'name': 'framing_option',
            }
        ),
        error_messages={'invalid': 'Invalid framing option'}
    )

    notes = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'e.g., "Gift wrapping requested"',
                'class': 'custom-input w-full h-20 resize-none',
                'id': 'notes',
                'name': 'notes',
                'maxlength': '500',
            }
        ),
        error_messages={'max_length': 'Notes cannot exceed 500 characters'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make framing_option field optional explicitly
        self.fields['framing_option'].required = False

    def clean_artwork_id(self):
        """Validate that artwork exists and is available"""
        artwork_id = self.cleaned_data.get('artwork_id')

        try:
            artwork = Artwork.objects.get(id=artwork_id)
            if not artwork.is_in_stock:
                raise ValidationError('This artwork is out of stock')
            return artwork_id
        except Artwork.DoesNotExist:
            raise ValidationError('Artwork not found')

    def clean_quantity(self):
        """Validate quantity against available stock"""
        quantity = self.cleaned_data.get('quantity')
        artwork_id = self.cleaned_data.get('artwork_id')

        if artwork_id:
            try:
                artwork = Artwork.objects.get(id=artwork_id)
                if quantity > artwork.quantity:
                    raise ValidationError(
                        f'Only {artwork.quantity} units available in stock'
                    )
            except Artwork.DoesNotExist:
                pass

        return quantity

    def clean_framing_option(self):
        """Validate that framing option exists if provided"""
        framing_option = self.cleaned_data.get('framing_option')

        if framing_option:
            try:
                ArtworkFramingCondition.objects.get(id=framing_option)
            except ArtworkFramingCondition.DoesNotExist:
                raise ValidationError('Invalid framing option')

        return framing_option

    def clean_notes(self):
        """Sanitize notes"""
        notes = self.cleaned_data.get('notes', '').strip()
        return notes


class UpdateCartQuantityForm(forms.Form):
    """
    Form for updating cart item quantity via API
    """

    artwork_id = forms.IntegerField(
        required=True,
        error_messages={'required': 'Artwork ID is required'}
    )

    quantity = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=999,
        error_messages={
            'required': 'Quantity is required',
            'min_value': 'Quantity must be at least 0',
            'max_value': 'Quantity cannot exceed 999',
            'invalid': 'Please enter a valid quantity',
        }
    )

    def clean_artwork_id(self):
        """Validate that artwork exists"""
        artwork_id = self.cleaned_data.get('artwork_id')

        try:
            Artwork.objects.get(id=artwork_id)
            return artwork_id
        except Artwork.DoesNotExist:
            raise ValidationError('Artwork not found')


class RemoveFromCartForm(forms.Form):
    """
    Form for removing item from cart via API
    """

    artwork_id = forms.IntegerField(
        required=True,
        error_messages={'required': 'Artwork ID is required'}
    )

    def clean_artwork_id(self):
        """Validate that artwork exists"""
        artwork_id = self.cleaned_data.get('artwork_id')
        try:
            Artwork.objects.get(id=artwork_id)
            return artwork_id
        except Artwork.DoesNotExist:
            raise ValidationError('Artwork not found')


class SyncCartForm(forms.Form):
    """
    Form for syncing cart with backend
    Cart data is passed as JSON in the request body
    """

    cart = forms.JSONField(
        required=True,
        error_messages={
            'required': 'Cart data is required',
            'invalid': 'Invalid cart JSON format'
        }
    )

    def clean_cart(self):
        """Validate cart structure"""
        cart = self.cleaned_data.get('cart')

        if not isinstance(cart, dict):
            raise ValidationError('Cart must be an object')

        # Validate each cart item
        for artwork_id, item in cart.items():
            if not isinstance(item, dict):
                msg = f'Invalid item format for artwork {artwork_id}'
                raise ValidationError(msg)

            if 'quantity' not in item or not isinstance(
                item['quantity'], int
            ):
                msg = f'Missing or invalid quantity for {artwork_id}'
                raise ValidationError(msg)

            if item['quantity'] <= 0:
                msg = f'Quantity must be positive for {artwork_id}'
                raise ValidationError(msg)

        return cart
