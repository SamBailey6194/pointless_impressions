from django.forms import ModelForm
from django import forms
from .models import Photo


# Define a form for the Photo model
class PhotoForm(ModelForm):
    """Form for uploading and editing photos."""
    class Meta:
        model = Photo
        fields = [
            'title',
            'description',
            'image',
            'alt_text'
            ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter description',
                'rows': 3
            }),
            'alt_text': forms.TextInput(attrs={
                'placeholder': 'Enter alt text for the image'
            }),
        }
