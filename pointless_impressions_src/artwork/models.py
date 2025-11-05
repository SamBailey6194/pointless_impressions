from django.db import models
from django.utils.text import slugify
import random
import string
from django.conf import settings
from pointless_impressions_src.photo.models import Photo
from pointless_impressions_src.profiles.models import Artist


# Create your models here.
class Artwork(models.Model):
    """Model to represent an artwork item."""
    name = models.CharField(max_length=255, unique=True, blank=False)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artworks'
    )
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    sku = models.CharField(max_length=100, unique=True, blank=False)
    category = models.ForeignKey(
        'ArtworkCategory', on_delete=models.SET_NULL, null=True, blank=True
    )
    selected_conditions = models.ManyToManyField(
        'ArtworkFramingCondition',
        blank=False,
        related_name='available_conditions',
        help_text="The set of framing/condition options available for "
        "customer selection."
    )
    main_photo = models.ForeignKey(
        'photo.Photo',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='main_for_artwork'
    )
    is_available = models.BooleanField(default=True)
    is_in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        """String representation of the Artwork model."""
        return self.name

    def save(self, *args, **kwargs):
        """
        Override save to generate SKU if not provided and set is_in_stock.
        """
        if not self.sku:
            self.sku = self.generate_unique_sku()
        if not self.slug:
            self.slug = slugify(self.name)
        # Set is_in_stock to True if quantity is not 0, else False
        self.is_in_stock = self.quantity != 0
        super().save(*args, **kwargs)

    def generate_unique_sku(self):
        """Generate a unique SKU for the artwork."""
        sku = self.generate_sku()
        while Artwork.objects.filter(sku=sku).exists():
            sku = self.generate_sku()
        return sku

    def generate_sku(self):
        """Generate a SKU for the artwork."""
        characters = string.ascii_uppercase + string.digits
        return "SKU-" + ''.join(random.choices(characters, k=10))

    def _get_primary_photo(self):
        """Retrieve the primary photo associated with this artwork."""
        if not hasattr(self, '_cached_photo'):
            if self.main_photo:
                self._cached_photo = self.main_photo
            else:
                self._cached_photo = Photo.objects.filter(artwork=self).first()
        return self._cached_photo

    @property
    def image(self):
        """Get the primary photo for this artwork."""
        photo = self._get_primary_photo()
        return photo.image if photo else None

    @property
    def image_url(self):
        """Get the URL of the primary photo."""
        photo = self._get_primary_photo()
        return photo.get_image_url if photo else ''

    @property
    def image_alt_text(self):
        """Get the alt text for the primary photo."""
        photo = self._get_primary_photo()
        return photo.alt_text_or_default if photo else self.name


class ArtworkCategory(models.Model):
    """Model to represent artwork categories."""
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255, unique=True, blank=False)
    friendly_name = models.CharField(
        max_length=255, blank=False, null=True
    )
    description = models.TextField(blank=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ArtworkFramingCondition(models.Model):
    """Model to represent framing options for artworks."""
    condition_name = models.CharField(max_length=255, blank=False)
    condition_friendly_name = models.CharField(
        max_length=255, blank=False, null=True
        )
    condition_description = models.TextField(blank=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.condition_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.condition_name}: {self.condition_description}"

    def get_friendly_name(self):
        return self.condition_friendly_name


class ArtworkReview(models.Model):
    """Model to represent reviews for artworks."""
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    review_text = models.TextField(blank=False)
    rating = models.PositiveIntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('artwork', 'reviewer')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.artwork.name} by {self.reviewer.username}"
