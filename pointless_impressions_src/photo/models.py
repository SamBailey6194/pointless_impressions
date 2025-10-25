from django.db import models
from django.forms import ValidationError
from django.conf import settings
from cloudinary.models import CloudinaryField
from pointless_impressions_src.artwork.models import Artwork
# from pointless_impressions_src.profile.models import Profile
# from pointless_impressions_src.blog.models import Blog


# Create your models here.
# Helper function to determine upload path based on associated model
def artwork_image_path(instance, filename):
    # if instance.artwork:
    #     return f"artwork/{filename}"
    # elif instance.profile:
    #     return f"profile/{filename}"
    # elif instance.blog:
    #     return f"blog/{filename}"
    # elif instance.account:
    #     return f"account/{filename}"
    # return f"others/{filename}"
    return f"artwork/{filename}"


# Photo model to store images associated with Artwork, Profile, or Blog
class Photo(models.Model):
    artwork = models.ForeignKey(
        Artwork,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    # profile = models.ForeignKey(
    #     Profile,
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE
    # )
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
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    if settings.DEBUG:
        # Dev: use local file storage
        image = models.ImageField(upload_to=artwork_image_path)
    else:
        # Staging/Prod: use Cloudinary
        image = CloudinaryField('image', folder=artwork_image_path)
    alt_text = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # String representation of the model
    def __str__(self):
        return f"Photo {self.title} uploaded at {self.uploaded_at}"

    # Validation to ensure only one parent is linked
    def clean(self):
        """Ensure the photo is linked to only one parent at a time."""
        parents = [
            bool(self.artwork),
            bool(self.profile),
            bool(self.blog),
            bool(self.account)
            ]
        if sum(parents) > 1:
            raise ValidationError(
                "Photo can only be linked to one parent at a time."
                )

    # Get the URL of the uploaded image
    @property
    def get_image_url(self):
        """Return the URL of the uploaded image."""
        if self.image:
            return self.image.url
        return ''

    # Get alt text or default based on parent
    @property
    def alt_text_or_default(self):
        """Fallback alt text based on parent if none provided."""
        if self.alt_text:
            return self.alt_text
        if self.artwork:
            return self.artwork.name
        if self.blog:
            return self.blog.title
        if self.profile:
            return self.profile.user.username
        return "Photo"
