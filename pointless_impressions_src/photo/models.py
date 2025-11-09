from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from cloudinary.models import CloudinaryField


# Create your models here.
def artwork_image_path(instance, filename):
    """Determine upload path based on associated model."""
    if instance.artwork:
        return f"artwork/{filename}"
    # elif instance.blog:
    #     return f"blog/{filename}"
    elif instance.account:
        return f"profiles/{filename}"
    elif instance.photo_type == 'site_asset':
        return f"site_assets/{filename}"
    return f"others/{filename}"


class Photo(models.Model):
    """
    Model to store photos linked to Artwork, Blog, Account, or Site Assets.
    """

    PHOTO_TYPE_CHOICES = [
        ('artwork', 'Artwork Image'),
        ('profile', 'Profile Picture'),
        ('site_asset', 'Site Asset (Logo, Banner, etc.)'),
        # ('blog', 'Blog Image'),
    ]
    artwork = models.ForeignKey(
        'artwork.Artwork',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    # blog = models.ForeignKey(
    #     Blog,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name='photos'
    # )

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

    # Use Cloudinary for all environments (staging/prod required)
    # CloudinaryField stores the Cloudinary URL in database
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
        if self.photo_type == 'artwork' and not self.artwork:
            raise ValidationError(
                "Artwork photos must be linked to an Artwork."
                )

        if self.photo_type == 'site_asset' and not self.asset_identifier:
            raise ValidationError(
                "Site assets must have an asset identifier."
                )

        # Ensure only one parent for non-site-asset photos
        if self.photo_type not in ['site_asset', 'profile']:
            parents = [
                bool(self.artwork),
                # bool(self.blog),
            ]
            if sum(parents) > 1:
                raise ValidationError(
                    "Photo can only be linked to one parent at a time."
                )

    def get_folder(self):
        """Determine Cloudinary folder based on photo type."""
        folder_map = {
            'artwork': 'artwork',
            'profile': 'profiles',
            'site_asset': 'site_assets',
            # 'blog': 'blog',
        }
        return folder_map.get(self.photo_type, 'others')

    def upload_options(self, overwrite=None):
        """Generate Cloudinary upload options based on photo type."""
        options = {
            'folder': self.get_folder(),
            'use_filename': True,
            'unique_filename': not (
                overwrite if overwrite is not None else False
                ),
            'resource_type': 'image',
        }
        return options

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
        # elif self.photo_type == 'blog' and self.blog:
        #     return self.blog.title
        elif self.photo_type == 'profile':
            if hasattr(self, 'user_profile'):
                username = self.user_profile.user.username
                return f"{username}'s profile picture"
            return "Profile picture"
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
