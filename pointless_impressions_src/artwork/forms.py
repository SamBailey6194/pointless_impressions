from django.forms import ModelForm
from django import forms
from .models import ArtworkReview


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
