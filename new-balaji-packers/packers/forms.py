import re
from datetime import date
from django import forms
from .models import BookingOrder, CustomerReview

STANDARD_ITEM_CHOICES = [
    ("Double Bed & Mattress", "🛏️ Double Bed & Mattress"),
    ("Single Bed & Cot", "🛏️ Single Bed & Cot"),
    ("Sofa Set (3+1+1)", "🛋️ Sofa Set (3+1+1)"),
    ("L-Shape Sofa", "🛋️ L-Shape Sofa"),
    ("Dining Table & Chairs", "🍽️ Dining Table & Chairs"),
    ("Refrigerator / Fridge", "🧊 Refrigerator / Fridge"),
    ("Washing Machine", "🧺 Washing Machine"),
    ("Smart TV & Wall Unit", "📺 Smart TV & Unit"),
    ("Split AC & Compressor", "❄️ Split AC & Outdoor Unit"),
    ("Wardrobe / Almirah", "🚪 Wardrobe / Almirah"),
    ("Kitchen Utensil Boxes", "📦 Kitchen Utensils & Cartons"),
    ("Clothing & Personal Boxes", "📦 Clothes & Suitcases"),
    ("Computer / Workstation", "💻 Computer / Study Desk"),
    ("Motorcycle / Scooty", "🏍️ Two-Wheeler / Bike"),
    ("Car / Automobile", "🚗 Four-Wheeler / Car"),
    ("Water Purifier & Geyser", "🚰 RO Purifier & Geyser"),
]

LOCATION_CHOICES = [
    ("", "-- Select Location --"),
    ("Vuyyuru", "Vuyyuru (Main Head Office)"),
    ("Vijayawada", "Vijayawada Branch"),
    ("Machilipatnam", "Machilipatnam Branch"),
    ("Gudur", "Gudur"),
    ("Pamarru", "Pamarru"),
    ("Kankipadu", "Kankipadu"),
    ("Gannavaram", "Gannavaram"),
    ("Guntur", "Guntur"),
    ("Tenali", "Tenali"),
    ("Mangalagiri", "Mangalagiri"),
    ("Hyderabad", "Hyderabad (Telangana)"),
    ("Bangalore", "Bangalore (Karnataka)"),
    ("Chennai", "Chennai (Tamil Nadu)"),
    ("Visakhapatnam", "Visakhapatnam (Vizag)"),
    ("Other", "Other Location (Specify in Notes)"),
]


class BookingOrderForm(forms.ModelForm):
    """
    ModelForm for customer relocation bookings with custom items and standard item checklists.
    """
    items_checklist = forms.MultipleChoiceField(
        choices=STANDARD_ITEM_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Select Standard Items to Move"
    )

    pickup_city = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg shadow-sm'}),
        label="Moving From (Origin / Pickup City)"
    )

    drop_city = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg shadow-sm'}),
        label="Moving To (Destination / Drop City)"
    )

    class Meta:
        model = BookingOrder
        fields = [
            'customer_name',
            'phone',
            'email',
            'pickup_city',
            'drop_city',
            'move_date',
            'move_type',
            'custom_items',
            'packing_tier',
            'floor_details',
            'estimated_price',
            'notes',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg shadow-sm',
                'placeholder': 'Enter your full name',
                'autocomplete': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg shadow-sm',
                'placeholder': '10-digit mobile number (e.g. 9014331173)',
                'type': 'tel',
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Optional: email for quotation & bills',
                'autocomplete': 'email',
            }),
            'move_date': forms.DateInput(attrs={
                'class': 'form-control form-control-lg shadow-sm',
                'type': 'date',
            }),
            'move_type': forms.Select(attrs={
                'class': 'form-select form-select-lg shadow-sm',
            }),
            'custom_items': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 3,
                'placeholder': 'E.g., 65-inch Curved OLED TV, Glass coffee table, 2 AC units, Pooja mandir, Aquarium, Gym equipment, Bicycle...',
            }),
            'packing_tier': forms.Select(attrs={
                'class': 'form-select shadow-sm',
            }),
            'floor_details': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'E.g. Ground to 2nd Floor (Lift Available at both ends)',
            }),
            'estimated_price': forms.NumberInput(attrs={
                'class': 'form-control fw-bold text-success shadow-sm',
                'readonly': 'readonly',
                'placeholder': 'Calculated by interactive price tool',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 2,
                'placeholder': 'Any specific instructions, parking access, timing preference, or GST bill request...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set min date to today for move_date
        self.fields['move_date'].widget.attrs['min'] = date.today().isoformat()
        if self.instance and self.instance.pk and self.instance.selected_items:
            # Pre-select items if editing existing
            selected = [i.strip() for i in self.instance.selected_items.split(',') if i.strip()]
            self.fields['items_checklist'].initial = selected

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        cleaned = re.sub(r'[^\d+]', '', phone)
        digits = re.sub(r'\D', '', cleaned)
        if len(digits) < 10:
            raise forms.ValidationError("Please provide a valid 10-digit mobile number.")
        return cleaned

    def clean_move_date(self):
        move_date = self.cleaned_data.get('move_date')
        if move_date and move_date < date.today():
            raise forms.ValidationError("Moving date cannot be in the past.")
        return move_date

    def clean(self):
        cleaned_data = super().clean()
        pickup = cleaned_data.get('pickup_city')
        drop = cleaned_data.get('drop_city')
        if pickup and drop and pickup == drop and pickup != 'Other':
            # Note: local shifting within the same city is allowed, but let's make sure it's valid
            pass
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected = self.cleaned_data.get('items_checklist', [])
        if selected:
            instance.selected_items = ", ".join(selected)
        if commit:
            instance.save()
        return instance


class CustomerReviewForm(forms.ModelForm):
    """
    Form for customer reviews with live star rating selector.
    """
    city = forms.ChoiceField(
        choices=[
            ("Vuyyuru", "Vuyyuru (Head Office)"),
            ("Vijayawada", "Vijayawada Branch"),
            ("Machilipatnam", "Machilipatnam Branch"),
            ("Intercity / Other", "Other Route / Intercity"),
        ],
        widget=forms.Select(attrs={'class': 'form-select shadow-sm'}),
        label="Service Location / Branch"
    )

    class Meta:
        model = CustomerReview
        fields = ['reviewer_name', 'city', 'rating', 'review_text']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Your Full Name',
                'required': 'required',
            }),
            'rating': forms.HiddenInput(attrs={
                'id': 'id_rating_input',
                'value': '5',
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'rows': 3,
                'placeholder': 'Share your experience with New Balaji Packers and Movers (packing quality, timing, staff behavior, vehicle safety)...',
                'required': 'required',
            }),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        try:
            rating = int(rating)
        except (ValueError, TypeError):
            rating = 5
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5 stars.")
        return rating
