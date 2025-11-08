from django.forms import ModelForm
from django import forms
from .models import ArtworkReview, Artwork, ArtworkFramingCondition


# Write your forms here
class ArtworkReviewForm(ModelForm):
    """Form for submitting artwork reviews."""
    class Meta:
        model = ArtworkReview
        fields = [
            'review_title',
            'rating',
            'review_text',
        ]
        widgets = {
            'review_title': forms.TextInput(attrs={
                'placeholder': 'Enter a review title',
                'class': 'custom-input',
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'type': 'hidden',
                'placeholder': 'Enter rating (1-5)'
            }),
            'review_text': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts about this artwork...',
                'rows': 4,
                'class': 'custom-input',
            }),
        }
        labels = {
            'review_title': 'Title',
            'rating': 'Rating',
            'review_text': 'Your Review',
        }

    def clean_review_title(self):
        review_title = self.cleaned_data.get('review_title')
        if not review_title or not review_title.strip():
            raise forms.ValidationError("Title cannot be empty.")
        if len(review_title.strip()) < 5:
            raise forms.ValidationError(
                "Title must be at least 5 characters long."
            )
        return review_title

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if not review_text or not review_text.strip():
            raise forms.ValidationError("Review cannot be empty.")
        if len(review_text.strip()) < 10:
            raise forms.ValidationError(
                "Review must be at least 10 characters long."
            )
        return review_text


class ArtworkForm(forms.ModelForm):
    """
    Form for admin staff to create and edit artwork.
    Includes all fields for full CRUD operations.
    """

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        error_messages={
            'invalid': 'Price must be a valid decimal number.',
            'min_value': 'Price must be greater than 0.',
        }
    )

    quantity = forms.IntegerField(
        min_value=0,
        initial=0,
        help_text='Number of pieces in stock'
    )

    selected_conditions = forms.ModelMultipleChoiceField(
        queryset=ArtworkFramingCondition.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select available framing conditions'
    )

    class Meta:
        model = Artwork
        fields = [
            'name',
            'artist',
            'description',
            'price',
            'category',
            'selected_conditions',
            'main_photo',
            'quantity',
            'is_available',
            'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Artwork title'
            }),
            'artist': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed description of the artwork'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'main_photo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_name(self):
        """Validate artwork name is not blank."""
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError(
                'Artwork name cannot be empty.'
            )
        return name

    def clean_description(self):
        """Validate description is not blank."""
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise forms.ValidationError(
                'Description cannot be empty.'
            )
        return description

    def clean_price(self):
        """Validate price is positive."""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError(
                'Price must be greater than 0.'
            )
        return price

    def clean_quantity(self):
        """Validate quantity is non-negative."""
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError(
                'Quantity cannot be negative.'
            )
        return quantity


class ArtworkSubmissionForm(forms.ModelForm):
    """
    Form for artists to submit artwork for approval.
    Limited to essential fields; excludes admin-only controls.
    """

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        help_text='Price in GBP',
        error_messages={
            'invalid': 'Price must be a valid decimal.',
            'min_value': 'Price must be greater than 0.',
        }
    )

    selected_conditions = forms.ModelMultipleChoiceField(
        queryset=ArtworkFramingCondition.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select framing condition options'
    )

    class Meta:
        model = Artwork
        fields = [
            'name',
            'description',
            'price',
            'category',
            'selected_conditions'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Artwork title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your artwork...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_name(self):
        """Validate name is unique (except for current instance)."""
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError(
                'Artwork name is required.'
            )
        # Check for duplicates
        qs = Artwork.objects.filter(name=name)
        if self.instance.id:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise forms.ValidationError(
                f'Artwork with name "{name}" already exists.'
            )
        return name

    def clean_price(self):
        """Validate price is reasonable."""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError(
                'Price must be greater than 0.'
            )
        if price is not None and price > 10000.00:
            raise forms.ValidationError(
                'Price seems unusually high. Please verify.'
            )
        return price

    def save(self, commit=True, artist=None):
        """
        Save artwork with artist and pending approval status.
        """
        artwork = super().save(commit=False)
        if artist:
            artwork.artist = artist
        artwork.is_available = False  # Pending approval
        if commit:
            artwork.save()
            self.save_m2m()  # Save framing conditions
        return artwork


class ArtworkApprovalForm(forms.ModelForm):
    """
    Form for admin staff to approve/reject submitted artwork.
    Limited to approval-related fields.
    """

    class Meta:
        model = Artwork
        fields = ['is_available']
        widgets = {
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'is_available': 'Approve artwork (make available for sale)'
        }

    def clean_is_available(self):
        """Validate approval status."""
        is_available = self.cleaned_data.get('is_available')
        return is_available
