from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from .models import (
    Artwork, ArtworkFramingCondition, ArtworkCategory
)


# Write your forms here.
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                HTML(
                    "<h2 class='card-title text-center mb-4 "
                    "text-(--pointless-black) dark:text-(--pointless-white)'>"
                    "Submit Artwork</h2>"
                ),
                Div(
                    HTML(
                        "<h4 class='mb-2 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>"
                        "Artwork Details</h4>"
                    ),
                    Div(
                        Field(
                            'name',
                            placeholder="Artwork Title",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'description',
                            placeholder="Describe your artwork...",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    HTML(
                        "<h4 class='mb-2 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>"
                        "Pricing and Category</h4>"
                    ),
                    Div(
                        Field(
                            'price',
                            placeholder="0.00",
                            css_class='mb-4 custom-input w-full lg:w-66'
                        ),
                        Field(
                            'category',
                            css_class='custom-input w-full lg:w-66'
                        ),
                        css_class='lg:flex lg:gap-4 mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    HTML(
                        "<h4 class='mb-2 text-(--pointless-black) "
                        "dark:text-(--pointless-white)'>"
                        "Framing Options</h4>"
                    ),
                    Div(
                        Field(
                            'selected_conditions',
                            css_class='custom-input w-full'
                        ),
                        css_class='mb-4'
                    ),
                    HTML(
                        "<div class='form-divider'></div>"
                    ),
                    css_class='flex flex-col gap-4'
                ),
                css_class='px-6 py-2 mb-4',
                id='artwork-submission-form'
            ),
        )

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
        Dynamically add new categories and framing conditions to the database.
        """
        artwork = super().save(commit=False)

        if artist:
            artwork.artist = artist

        artwork.is_available = False

        category_name = self.cleaned_data.get('category')
        if category_name:
            if isinstance(category_name, str) and category_name.strip():
                category, created = ArtworkCategory.objects.get_or_create(
                    name=category_name.strip()
                )
                artwork.category = category

        if commit:
            artwork.save()
            self.save_m2m()

        return artwork


class AddToCartForm(forms.Form):
    """
    Form for adding items to cart via detail page.
    Validates artwork, quantity, framing options, and notes.
    Uses a dynamic __init__ to set choices based on the artwork.
    """
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label=False,
        widget=forms.NumberInput(
            attrs={
                'class': 'text-center custom-input !w-24'
            })
    )

    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'class': 'custom-input'
            }),
        required=False,
        label=False
    )

    def __init__(self, *args, **kwargs):
        """
        Override __init__ to accept an artwork_id, which is used
        to fetch the artwork and dynamically set form fields.
        """
        artwork_id = kwargs.pop('artwork_id', None)
        super().__init__(*args, **kwargs)

        if not artwork_id:
            raise ValueError("artwork_id is required for AddToCartForm")

        try:
            self.artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
            raise ValueError(f"Invalid artwork_id: {artwork_id}")

        available_conditions = self.artwork.selected_conditions.all()

        if available_conditions.exists():
            self.fields['framing_option'] = forms.ModelChoiceField(
                queryset=available_conditions,
                label=False,
                widget=forms.Select,
                empty_label=None,
                initial=available_conditions.first(),
                required=True
            )
            self.fields['framing_option'].label_from_instance = \
                lambda obj: obj.condition_friendly_name
        else:
            pass

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        layout_items = [
            HTML("""
                <label for="id_quantity"
                 class="font-bold
                 text-lg
                 text-(--pointless-black)
                 dark:text-(--pointless-white)">
                 Quantity
                </label>
            """),
            Div(
                HTML(
                    """
                    <div class="flex items-center space-x-2">
                        <button type="button"
                                class="btn btn-outline"
                                id="decrement-quantity"
                                aria-label="Decrease quantity">
                            -
                        </button>
                        <input type="number"
                               name="quantity"
                               id="id_quantity"
                               class="text-center custom-input !w-24"
                               value="1"
                               min="1">
                        <button type="button"
                                class="btn btn-outline"
                                id="increment-quantity"
                                aria-label="Increase quantity">
                            +
                        </button>
                    </div>
                    """
                ),
                css_class="mb-4"
            ),
        ]

        if 'framing_option' in self.fields:
            framing_choices = self.fields['framing_option'].choices
            layout_items.append(
                HTML(f"""
                    <div>
                        <label for="id_framing_option"
                        class="font-bold
                        text-lg
                        text-(--pointless-black)
                        dark:text-(--pointless-white)">
                        Framing Options
                        </label>
                    </div>
                    <div>
                        <select class="select-dropdown w-full"
                        name="framing_option"
                        id="id_framing_option">
                            {''.join([
                                f'<option value="{option[0]}" '
                                f'{
                                    "selected" if option[0] == self.initial.
                                    get(
                                        "framing_option"
                                        ) else ""
                                    }'
                                f'>{option[1]}</option>'
                                for option in framing_choices
                            ])}
                        </select>
                    </div>
                """),
            )

        layout_items.append(
            HTML("""
                 <label for="id_notes"
                       class="font-bold text-lg
                              text-[var(--pointless-black)]
                              dark:text-[var(--pointless-white)]">
                    Notes
                </label>
            """),
        )
        layout_items.append(
            Div(
                Field('notes'),
                css_class="mb-4"
            )
        )

        layout_items.append(
            HTML("""
                <button type="submit" name="submit"
                        class="mb-4 btn btn-ghost btn-outline">
                    <i class="fa-solid fa-cart-plus"></i> Add to Cart
                </button>
            """)
        )

        # Pass stock to the form's initial data
        self.helper.layout = Layout(
            *layout_items,
            HTML(
                f"<input type='hidden' id='stock_quantity' "
                f"value='{self.artwork.stock}'>"
            )
        )

    def clean_quantity(self):
        """
        Custom validation for the quantity field.
        Checks that the requested quantity is available in stock.
        """
        quantity = self.cleaned_data.get('quantity')
        stock = self.artwork.quantity

        if quantity is None:
            raise forms.ValidationError("Quantity is required.")

        if not self.artwork.is_in_stock or stock == 0:
            raise forms.ValidationError("This item is out of stock.")

        if quantity > stock:
            raise forms.ValidationError(
                f"Only {stock} available in stock. "
                f"Please reduce your quantity."
            )
        return quantity

    def clean_framing_option(self):
        """
        Custom validation for the framing_option field.
        Ensures the selected option is valid for this artwork.
        """
        framing_option = self.cleaned_data.get('framing_option')

        if not framing_option:
            return None

        if framing_option not in self.artwork.selected_conditions.all():
            raise forms.ValidationError(
                "That is not a valid framing option for this artwork."
            )

        return framing_option

    def is_valid(self):
        """
        Override is_valid to add debugging for the validation process.
        """
        valid = super().is_valid()
        return valid
