from django.db import models
from django.forms import ValidationError
from django.conf import settings
from cloudinary.models import CloudinaryField
from pointless_impressions_src.artwork.models import Artwork
# from pointless_impressions_src.blog.models import Blog


# Create your models here.
def artwork_image_path(instance, filename):
    """Determine upload path based on associated model."""
    if instance.artwork:
        return f"artwork/{filename}"
    # elif instance.blog:
    #     return f"blog/{filename}"
    elif instance.account:
        return f"account/{filename}"
    return f"others/{filename}"


class Photo(models.Model):
    """Model to store photos linked to Artwork, Blog, or Account."""
    artwork = models.ForeignKey(
        Artwork,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    # blog = models.ForeignKey(
    #     Blog,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE
    # )
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=False)
    if settings.DEBUG:
        # Dev: use local file storage
        image = models.ImageField(upload_to=artwork_image_path)
    else:
        # Staging/Prod: use Cloudinary
        image = CloudinaryField('image', folder=artwork_image_path)
    alt_text = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Photo model."""
        return f"Photo {self.title} uploaded at {self.uploaded_at}"

    def clean(self):
        """Ensure the photo is linked to only one parent at a time."""
        parents = [
            bool(self.artwork),
            bool(self.blog),
            bool(self.account)
            ]
        if sum(parents) > 1:
            raise ValidationError(
                "Photo can only be linked to one parent at a time."
                )

    @property
    def get_image_url(self):
        """Return the URL of the uploaded image."""
        if self.image:
            return self.image.url
        return ''

    @property
    def alt_text_or_default(self):
        """Fallback alt text based on parent if none provided."""
        if self.alt_text:
            return self.alt_text
        if self.artwork:
            return self.artwork.name
        if self.blog:
            return self.blog.title
        if self.account:
            return self.account.username
        return "Photo"
