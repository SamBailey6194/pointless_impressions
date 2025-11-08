from django.forms import ModelForm
from django import forms
from .models import Photo


class PhotoForm(ModelForm):
    """
    Base form for uploading and editing photos.
    DRY approach: conditionally include fields based on photo_type.
    Supports artwork, profile, site_asset photos.
    """

    overwrite = forms.BooleanField(
        required=False,
        initial=False,
        label="Overwrite existing file with same name?",
        help_text="If checked, this upload will replace any existing file with"
        " the same name/public_id."
    )

    class Meta:
        model = Photo
        fields = [
            'photo_type',
            'title',
            'description',
            'image',
            'alt_text',
            'artwork',
            'asset_identifier'
        ]
        widgets = {
            'photo_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_photo_type'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter alt text for the image'
            }),
            'artwork': forms.Select(attrs={
                'class': 'form-control'
            }),
            'asset_identifier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., logo_main, banner_home'
            })
        }

    def __init__(self, *args, photo_type=None, **kwargs):
        """
        Initialize form with conditional fields based on photo_type.
        This allows different forms to use only needed fields.
        """
        super().__init__(*args, **kwargs)
        self.photo_type = photo_type or self.instance.photo_type

        # Always include base fields
        base_fields = {
            'photo_type', 'title', 'description', 'image', 'alt_text'
        }

        # Define fields per photo type
        type_fields_map = {
            'artwork': base_fields | {'artwork'},
            'profile': base_fields,
            'site_asset': base_fields | {'asset_identifier'},
        }

        # Get fields to include for this type
        allowed_fields = type_fields_map.get(
            self.photo_type,
            base_fields
        )

        # Remove fields not needed for this type
        for field in list(self.fields.keys()):
            if field not in allowed_fields:
                del self.fields[field]

        # Set field requirements based on type
        if self.photo_type == 'artwork':
            self.fields['artwork'].required = True
        elif self.photo_type == 'site_asset':
            self.fields['asset_identifier'].required = True

    def clean_title(self):
        """Validate title is not blank."""
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError('Title cannot be empty.')
        if len(title.strip()) < 3:
            raise forms.ValidationError(
                'Title must be at least 3 characters long.'
            )
        return title

    def clean_description(self):
        """Validate description."""
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise forms.ValidationError('Description cannot be empty.')
        if len(description.strip()) < 5:
            raise forms.ValidationError(
                'Description must be at least 5 characters long.'
            )
        return description

    def clean_alt_text(self):
        """Validate alt text."""
        alt_text = self.cleaned_data.get('alt_text')
        if alt_text and len(alt_text.strip()) > 255:
            raise forms.ValidationError(
                'Alt text must be 255 characters or less.'
            )
        return alt_text

    def clean_artwork(self):
        """Validate artwork field for artwork photos."""
        if self.photo_type == 'artwork':
            artwork = self.cleaned_data.get('artwork')
            if not artwork:
                raise forms.ValidationError(
                    'Artwork must be selected for artwork photos.'
                )
        return self.cleaned_data.get('artwork')

    def clean_asset_identifier(self):
        """Validate asset identifier for site assets."""
        if self.photo_type == 'site_asset':
            asset_identifier = self.cleaned_data.get('asset_identifier')
            if not asset_identifier or not asset_identifier.strip():
                raise forms.ValidationError(
                    'Asset identifier is required for site assets.'
                )
        return self.cleaned_data.get('asset_identifier')

    def clean(self):
        """Overall form validation."""
        cleaned_data = super().clean()
        photo_type = cleaned_data.get('photo_type')

        # Validate photo type constraints
        if photo_type == 'artwork':
            if not cleaned_data.get('artwork'):
                self.add_error(
                    'artwork',
                    'Artwork must be selected.'
                )

        elif photo_type == 'site_asset':
            if not cleaned_data.get('asset_identifier'):
                self.add_error(
                    'asset_identifier',
                    'Asset identifier is required.'
                )

        return cleaned_data

    def save(self, commit=True, user=None):
        """Save photo with user assignment if provided."""
        photo = super().save(commit=False)
        if user:
            photo.uploaded_by = user
        if commit:
            photo.save()
        return photo
