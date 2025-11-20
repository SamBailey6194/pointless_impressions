from django import forms
from .countries import COUNTRY_CHOICES
from .phone_prefix import PHONE_PREFIX_CHOICES


# Write your widgets here.
class CountrySelectFormWidget(forms.Select):
    """
    Custom widget for country selection with Crispy Forms styling.
    """
    def __init__(self, attrs=None, layout=None):
        default_classes = (
            'custom-input '
            'w-full '
            'lg:w-64 '
            'rounded-lg '
        )

        css_classes = layout or default_classes

        if attrs is None:
            attrs = {}
        attrs['class'] = css_classes

        super().__init__(attrs=attrs, choices=COUNTRY_CHOICES)

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        """
        Override the create_option method to disable specific options.
        """
        option_dict = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )

        # Disable "Select Country" and "---------------"
        if value in ('', '---------------'):
            option_dict['attrs']['disabled'] = True

        return option_dict


class PhonePrefixSelectFormWidget(forms.Select):
    """
    Custom widget for phone prefix selection with Crispy Forms styling.
    """
    def __init__(self, attrs=None, layout=None):
        default_classes = (
            'custom-input '
            'w-full '
            'lg:w-32 '
            'rounded-lg '
        )

        css_classes = layout or default_classes

        if attrs is None:
            attrs = {}
        attrs['class'] = css_classes

        super().__init__(attrs=attrs, choices=PHONE_PREFIX_CHOICES)

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        """
        Override the create_option method to disable specific options.
        """
        option_dict = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )

        # Disable "Select Prefix" and "---------------"
        if value in ('', '---------------'):
            option_dict['attrs']['disabled'] = True

        return option_dict


class PhoneMultiWidget(forms.MultiWidget):
    """
    A MultiWidget that combines PhonePrefixSelectFormWidget and a TextInput
    to create a complete phone number input.
    """
    def __init__(self, attrs=None):
        widgets = (
            PhonePrefixSelectFormWidget(attrs=attrs),
            forms.TextInput(attrs={
                'placeholder': 'e.g., 7123 456789',
                'class': 'custom-input w-full lg:w-48 rounded-lg',
                **(attrs or {})
            }),
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        """
        Splits the database value into parts for the widget.
        e.g., "+447123456789" -> ["+44", "7123456789"]
        """
        if value:
            sorted_prefixes = sorted(
                [p[0] for p in PHONE_PREFIX_CHOICES if p[0]],
                key=len,
                reverse=True
            )
            for prefix in sorted_prefixes:
                if value.startswith(prefix):
                    return [prefix, value[len(prefix):]]

            return [None, value]
        return ['+44', '']
