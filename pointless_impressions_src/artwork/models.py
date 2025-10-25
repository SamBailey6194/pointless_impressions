from django.db import models
import random
import string


# Create your models here.
class Artwork(models.Model):
    """Model to represent an artwork item."""
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    sku = models.CharField(max_length=100, unique=True, blank=False)
    category = models.ForeignKey(
        'ArtworkCategory', on_delete=models.SET_NULL, null=True, blank=True
    )
    selected_condition = models.ForeignKey(
        'ArtworkFramingCondition',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='artwork_condition'
    )
    is_available = models.BooleanField(default=True)
    is_in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the Artwork model."""
        return self.name

    def save(self, *args, **kwargs):
        """Override save to generate SKU if not provided."""
        if not self.sku:
            self.sku = self.generate_sku()
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


class ArtworkCategory(models.Model):
    """Model to represent artwork categories."""
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255, unique=True, blank=False)
    friendly_name = models.CharField(
        max_length=255, blank=False, null=True
    )
    description = models.TextField(blank=False)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class ArtworkFramingCondition(models.Model):
    """Model to represent framing options for artworks."""
    condition_name = models.CharField(max_length=255, blank=False)
    condition_description = models.TextField(blank=False)

    def __str__(self):
        return f"{self.condition_name}: {self.condition_description}"
