import uuid
from django.db import models
from django.utils import timezone


class Branch(models.Model):
    """
    Branch details for New Balaji Packers and Movers.
    Head office is Vuyyuru; Vijayawada and Machilipatnam are branches.
    """
    city = models.CharField(max_length=100, verbose_name="Branch City")
    is_head_office = models.BooleanField(
        default=False, 
        verbose_name="Is Head Office / Main Branch",
        help_text="Check if this branch is the Head Office (Vuyyuru)"
    )
    badge_text = models.CharField(
        max_length=100, 
        default="Branch Office",
        verbose_name="Badge Tag"
    )
    address = models.TextField(verbose_name="Full Physical Address")
    phone = models.CharField(max_length=20, verbose_name="Primary Phone")
    alt_phone = models.CharField(max_length=20, blank=True, verbose_name="Alternate Phone")
    manager_name = models.CharField(max_length=100, default="Mr. Kumar", verbose_name="Proprietor / In-charge")
    email = models.EmailField(blank=True, default="newbalajipackers@gmail.com", verbose_name="Branch Email")
    landmark = models.CharField(max_length=150, blank=True, verbose_name="Landmark")
    service_hours = models.CharField(max_length=100, default="24/7 Available (All Days)", verbose_name="Operating Hours")
    display_order = models.PositiveSmallIntegerField(default=1, verbose_name="Display Order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ['display_order', '-is_head_office', 'city']

    def __str__(self):
        role = "Head Office" if self.is_head_office else "Branch"
        return f"{self.city} ({role}) - {self.phone}"


class BookingOrder(models.Model):
    """
    Customer booking order model for relocations and quote requests.
    Supports standard items, custom item inputs, price calculations, and CSRF protection.
    """
    MOVE_TYPES = [
        ('household', 'Household Articles Shifting'),
        ('office', 'Office Relocation & Equipment Shifting'),
        ('car', 'Car / Vehicle Transportation'),
        ('local', 'Local City Shifting'),
        ('intercity', 'Intercity & All India Relocation'),
    ]

    PACKING_TIERS = [
        ('standard', 'Standard Packing (Cartons & High-Tack Tape)'),
        ('premium', 'Premium Multi-Layer (Bubble Wrap + Foam + Stretch Wrap)'),
        ('wooden_crate', 'Heavy Duty Custom Crate (Fragile & Electronics)'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending Quote Review'),
        ('Confirmed', 'Confirmed / Scheduled'),
        ('In Transit', 'In Transit / Moving'),
        ('Delivered', 'Delivered & Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    booking_ref = models.CharField(max_length=25, unique=True, blank=True, verbose_name="Booking Reference")
    customer_name = models.CharField(max_length=120, verbose_name="Your Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(blank=True, verbose_name="Email Address (Optional)")
    pickup_city = models.CharField(max_length=100, verbose_name="Moving From (Pickup City)")
    drop_city = models.CharField(max_length=100, verbose_name="Moving To (Drop City)")
    move_date = models.DateField(verbose_name="Scheduled Moving Date")
    move_type = models.CharField(max_length=80, choices=MOVE_TYPES, default='household', verbose_name="Type of Move")
    
    # Items selection & custom item input
    selected_items = models.TextField(
        blank=True, 
        verbose_name="Standard Selected Items",
        help_text="Standard household items selected by customer"
    )
    custom_items = models.TextField(
        blank=True, 
        verbose_name="Custom / Other Items",
        help_text="Custom, unusual or extra items specified by customer"
    )
    packing_tier = models.CharField(
        max_length=50, 
        choices=PACKING_TIERS, 
        default='premium', 
        verbose_name="Packing Quality"
    )
    floor_details = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Floor & Elevator Info",
        help_text="E.g., 2nd floor with lift, Ground floor"
    )
    
    estimated_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Estimated Price (₹)"
    )
    notes = models.TextField(blank=True, verbose_name="Special Instructions / Floor Details")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending', verbose_name="Order Status")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Booked At")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking Order"
        verbose_name_plural = "Booking Orders"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_part = uuid.uuid4().hex[:6].upper()
            self.booking_ref = f"NBP-{date_str}-{unique_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_ref} - {self.customer_name} ({self.pickup_city} → {self.drop_city})"


class CustomerReview(models.Model):
    """
    Customer ratings and feedback model with 1-5 star rating selector.
    """
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Fair'),
        (3, '3 Stars - Good'),
        (4, '4 Stars - Very Good'),
        (5, '5 Stars - Outstanding'),
    ]

    reviewer_name = models.CharField(max_length=100, verbose_name="Customer Name")
    city = models.CharField(max_length=100, default="Vuyyuru", verbose_name="City / Branch")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5, verbose_name="Star Rating")
    review_text = models.TextField(verbose_name="Customer Review")
    is_approved = models.BooleanField(default=True, verbose_name="Approved for Display")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted On")

    class Meta:
        verbose_name = "Customer Review"
        verbose_name_plural = "Customer Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer_name} ({self.rating}★) - {self.city}"
