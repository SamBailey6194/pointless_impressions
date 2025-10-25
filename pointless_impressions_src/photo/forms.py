from django.forms import ModelForm
from cloudinary.forms import CloudinaryFileField
from .models import Photo


# Define a form for the Photo model
class PhotoForm(ModelForm):
    image = CloudinaryFileField()

    class Meta:
        model = Photo
        fields = [
            'title',
            'description',
            'image',
            'alt_text'
            ]
