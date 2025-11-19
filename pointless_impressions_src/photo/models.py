from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from cloudinary.models import CloudinaryField


# Create your models here.
class Photo(models.Model):
    """
    Model to store photos linked to Artwork, Account, or Site Assets.
    """

    PHOTO_TYPE_CHOICES = [
        ('artwork', 'Artwork Image'),
        ('profile', 'Profile Picture'),
        ('site_asset', 'Site Asset (Logo, Banner, etc.)'),
    ]
    artwork = models.ForeignKey(
        'artwork.Artwork',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    user_profile = models.ForeignKey(
        'profiles.UserProfile',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    # For site assets (logos, banners, etc.)
    photo_type = models.CharField(
        max_length=20,
        choices=PHOTO_TYPE_CHOICES,
        default='artwork',
        help_text="Type of photo being uploaded"
    )

    # Optional: asset identifier for site assets
    asset_identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Identifier for site assets "
        "(e.g., 'logo_main', 'banner_home')"
    )

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)

    image = CloudinaryField(
        'image',
        blank=False,
        null=False
    )

    alt_text = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_photos',
        help_text="User who uploaded this photo"
    )

    def __str__(self):
        """String representation of the Photo model."""
        return f"{self.get_photo_type_display()}: {self.title}"

    def clean(self):
        """Validate photo linkage based on type."""
        if self.photo_type not in ['site_asset', 'profile']:
            parents = [
                bool(self.artwork),
            ]
            if sum(parents) > 1:
                raise ValidationError(
                    "Photo can only be linked to one parent at a time."
                )

    def get_folder(self):
        """Determine Cloudinary folder based on photo type."""
        folder_map = {
            'artwork': 'pointless-impressions-local/artwork',
            'profile': 'pointless-impressions-local/profiles',
            'site_asset': 'pointless-impressions-local/site_assets',
        }
        return folder_map.get(
            self.photo_type, 'pointless-impressions-local/others'
            )

    def get_upload_options(self):
        """Get Cloudinary upload options based on photo type."""
        return {
            'folder': self.get_folder(),
            'use_filename': True,
            'unique_filename': False,
            'resource_type': 'image',
        }

    def save(self, *args, **kwargs):
        """Override save to set Cloudinary options before upload."""
        if self.image:
            image_field = self._meta.get_field('image')

            if hasattr(image_field, 'options'):
                image_field.options.update(self.get_upload_options())

        super().save(*args, **kwargs)

    @property
    def get_image_url(self):
        """Return the URL of the uploaded image."""
        if self.image:
            return self.image.url
        return ''

    @property
    def alt_text_or_default(self):
        """Fallback alt text based on photo type and parent."""
        if self.alt_text:
            return self.alt_text

        if self.photo_type == 'artwork' and self.artwork:
            return self.artwork.name
        elif self.photo_type == 'profile' and self.user_profile:
            username = self.user_profile.user.username
            return f"{username}'s profile picture"
        elif self.photo_type == 'site_asset':
            return self.asset_identifier or "Site asset"

        return "Photo"

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['photo_type']),
            models.Index(fields=['asset_identifier']),
        ]
