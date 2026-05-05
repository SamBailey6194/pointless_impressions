from django.forms import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML
from .models import Photo


class BasePhotoForm(ModelForm):
    """
    Base form for photo uploads, providing shared logic and layout.
    """

    overwrite = forms.BooleanField(
        required=False,
        initial=False,
        label="",
    )

    class Meta:
        model = Photo
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ""
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    *self.get_layout_fields(),
                    css_class='flex flex-col gap-4'
                ),
                css_class='p-6 mb-6',
                id=self.get_form_id()
            )
        )

    def get_layout_fields(self):
        """Define layout fields in subclasses."""
        return []

    def get_form_id(self):
        """Define form ID in subclasses."""
        return 'base-photo-form'

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if len(description) < 5:
            raise forms.ValidationError("Description must be at least 5 characters long.")
        return description


class ProfilePhotoForm(BasePhotoForm):
    """
    Form for uploading profile photos.
    """

    class Meta(BasePhotoForm.Meta):
        fields = ['image', 'photo_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

        self.fields['photo_type'].initial = 'profile'
        self.fields['photo_type'].widget = forms.HiddenInput()
        self.fields['photo_type'].label = ''

    def get_layout_fields(self):
        return [
            HTML(
                "<h3 class='mb-2 text-(--pointless-black) "
                "dark:text-(--pointless-white)'>Profile Photo</h3>"
            ),
            Field(
                'image',
                css_class='mb-4 custom-input w-fit btn btn-ghost btn-outline'
            ),
            Field('photo_type'),
            HTML("<div class='form-divider'></div>"),
        ]

    def get_form_id(self):
        return 'profile-photo-form'

    def save(self, commit=True, user=None, user_profile=None):
        """
        Save the photo with automatic defaults.
        Only creates a Photo object if an image was uploaded.
        Returns None if no image was provided.
        """
        # Check if an image was uploaded; if not, return None
        if not self.cleaned_data.get('image'):
            return None

        photo = super().save(commit=False)

        if user:
            photo.title = f"{user.username}'s Profile Picture"
            photo.description = f"Profile picture for {user.username}"
            photo.alt_text = f"Profile picture of {user.username}"
        else:
            photo.title = "Profile Picture"
            photo.description = "User profile picture"
            photo.alt_text = "User profile picture"

        if user_profile:
            photo.user_profile = user_profile
            photo.artwork = None

        photo.photo_type = 'profile'

        if commit:
            photo.save()

            if user_profile:
                user_profile.profile_picture = photo
                user_profile.save()

        return photo


class AssetPhotoForm(BasePhotoForm):
    """
    Form for uploading site assets.
    """

    class Meta(BasePhotoForm.Meta):
        fields = [
            'title',
            'description',
            'image',
            'alt_text',
            'asset_identifier',
            'photo_type',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo_type'].initial = 'site_asset'
        self.fields['photo_type'].widget = forms.HiddenInput()
        self.fields['photo_type'].label = ''

    def get_layout_fields(self):
        return [
            HTML(
                "<h3 class='mb-2 text-(--pointless-black) "
                "dark:text-(--pointless-white)'>Asset Photo</h3>"
            ),
            Field(
                'image',
                css_class='mb-4 custom-input w-full'
            ),
            Field(
                'alt_text',
                placeholder="Describe the image for accessibility",
                css_class='mb-4 custom-input w-full'
            ),
            HTML("<div class='form-divider'></div>"),
            Field(
                'title',
                placeholder="Enter a descriptive title",
                css_class='mb-4 custom-input w-full lg:w-66'
            ),
            Field(
                'description',
                placeholder="Provide a detailed description",
                css_class='mb-4 custom-input w-full'
            ),
            HTML("<div class='form-divider'></div>"),
            Field(
                'asset_identifier',
                placeholder="e.g., logo_main, banner_home",
                css_class='mb-4 custom-input w-full lg:w-66'
            ),
            Field('photo_type'),
        ]

    def get_form_id(self):
        return 'asset-photo-form'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('asset_identifier'):
            self.add_error('asset_identifier', "Asset identifier is required for site assets.")
        return cleaned_data

    def save(self, commit=True, **kwargs):
        """
        Override save to set photo_type to 'site_asset'.
        """
        photo = super().save(commit=False)
        photo.photo_type = 'site_asset'

        if commit:
            photo.save()

        return photo


class ArtworkPhotoForm(BasePhotoForm):
    """
    Form for uploading artwork photos.
    """

    class Meta(BasePhotoForm.Meta):
        fields = ['title', 'description', 'image', 'alt_text', 'artwork', 'photo_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo_type'].initial = 'artwork'
        self.fields['photo_type'].widget = forms.HiddenInput()
        self.fields['photo_type'].label = ''

    def get_layout_fields(self):
        return [
            HTML(
                "<h3 class='mb-2 text-(--pointless-black) "
                "dark:text-(--pointless-white)'>Artwork Photo</h3>"
            ),
            Field(
                'image',
                css_class='mb-4 custom-input w-full'
            ),
            Field(
                'alt_text',
                placeholder="Describe the image for accessibility",
                css_class='mb-4 custom-input w-full'
            ),
            HTML("<div class='form-divider'></div>"),
            Field(
                'title',
                placeholder="Enter a descriptive title",
                css_class='mb-4 custom-input w-full lg:w-66'
            ),
            Field(
                'description',
                placeholder="Provide a detailed description",
                css_class='mb-4 custom-input w-full'
            ),
            Field('photo_type'),
            HTML("<div class='form-divider'></div>"),
        ]

    def get_form_id(self):
        return 'artwork-photo-form'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('artwork'):
            self.add_error('artwork', "Artwork must be selected for artwork photos.")
        return cleaned_data

    def save(self, commit=True, **kwargs):
        """
        Override save to set photo_type to 'artwork'.
        """
        photo = super().save(commit=False)
        photo.photo_type = 'artwork'

        if commit:
            photo.save()

        return photo
