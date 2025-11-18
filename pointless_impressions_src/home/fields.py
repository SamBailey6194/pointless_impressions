from django import forms
from django.core.exceptions import ValidationError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from pointless_impressions_src.home.widgets import PhoneMultiWidget


# Write your custom form fields here.
class CustomPhoneField(forms.CharField):
    """
    A custom form field that uses PhoneMultiWidget and validates
    the combined phone number.
    """
    widget = PhoneMultiWidget

    def clean(self, value):
        """
        The 'value' from a MultiWidget is a list.
        e.g., ['+44', '07123 456 789']
        """
        if not value or not isinstance(value, list) or len(value) != 2:
            raise ValidationError('Invalid phone number data.')

        prefix, number = value

        if not prefix or prefix in ('', '---------------'):
            raise ValidationError('Please select a country prefix.')

        if not number or number.strip() == '':
            raise ValidationError('Please enter your phone number.')

        cleaned_number = (
            number.strip().
            replace(' ', '').
            replace('-', '').
            replace('(', '').
            replace(')', '')
            )

        # Remove leading zero from the national number
        if cleaned_number.startswith('0'):
            cleaned_number = cleaned_number[1:]

        full_number_string = f"{prefix}{cleaned_number}"

        try:
            parsed_number = phonenumbers.parse(full_number_string, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError('Please enter a valid phone number.')
        except NumberParseException:
            raise ValidationError('Please enter a valid phone number format.')

        return full_number_string
