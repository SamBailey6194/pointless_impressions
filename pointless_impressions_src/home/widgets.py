from django import forms
from .countries import COUNTRY_CHOICES


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
