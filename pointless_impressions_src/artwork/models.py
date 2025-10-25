from django.db import models


# Create your models here.
class Artwork(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(upload_to='artwork_images/')
    is_available = models.BooleanField(default=True)
    is_in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    friendly_name = models.CharField(
        max_length=255, blank=True, null=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name
