from django.contrib import admin
from .models import Branch, BookingOrder, CustomerReview


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('city', 'is_head_office', 'badge_text', 'phone', 'manager_name', 'service_hours', 'display_order')
    list_editable = ('badge_text', 'phone', 'display_order')
    list_filter = ('is_head_office', 'city')
    search_fields = ('city', 'address', 'phone', 'manager_name', 'landmark')
    ordering = ('display_order', '-is_head_office', 'city')
    fieldsets = (
        ("Branch Core Identity", {
            "fields": ("city", "is_head_office", "badge_text", "display_order")
        }),
        ("Location & Contact", {
            "fields": ("address", "landmark", "phone", "alt_phone", "email", "manager_name", "service_hours")
        }),
    )


@admin.register(BookingOrder)
class BookingOrderAdmin(admin.ModelAdmin):
    list_display = (
        'booking_ref', 
        'customer_name', 
        'phone', 
        'pickup_city', 
        'drop_city', 
        'move_date', 
        'move_type', 
        'estimated_price', 
        'status', 
        'created_at'
    )
    list_filter = ('status', 'move_type', 'pickup_city', 'drop_city', 'packing_tier')
    search_fields = (
        'booking_ref', 
        'customer_name', 
        'phone', 
        'email', 
        'pickup_city', 
        'drop_city', 
        'custom_items', 
        'selected_items',
        'notes'
    )
    list_editable = ('status',)
    readonly_fields = ('booking_ref', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ("Booking Reference & Status", {
            "fields": ("booking_ref", "status", "created_at", "updated_at")
        }),
        ("Customer Details", {
            "fields": ("customer_name", "phone", "email")
        }),
        ("Relocation Route & Schedule", {
            "fields": ("pickup_city", "drop_city", "move_date", "move_type", "floor_details")
        }),
        ("Items to Shift (Standard & Custom)", {
            "fields": ("selected_items", "custom_items", "packing_tier")
        }),
        ("Financials & Notes", {
            "fields": ("estimated_price", "notes")
        }),
    )

    actions = ['mark_confirmed', 'mark_in_transit', 'mark_delivered']

    @admin.action(description="Mark selected orders as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status='Confirmed')

    @admin.action(description="Mark selected orders as In Transit")
    def mark_in_transit(self, request, queryset):
        queryset.update(status='In Transit')

    @admin.action(description="Mark selected orders as Delivered")
    def mark_delivered(self, request, queryset):
        queryset.update(status='Delivered')


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'city', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'city')
    search_fields = ('reviewer_name', 'review_text', 'city')
    list_editable = ('is_approved',)
    actions = ['approve_reviews', 'unapprove_reviews']

    @admin.action(description="Approve selected reviews for public display")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Hide/Unapprove selected reviews")
    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
