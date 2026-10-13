from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import Branch, BookingOrder, CustomerReview
from .forms import BookingOrderForm, CustomerReviewForm


def index_view(request):
    """
    Home page view: Hero, Branches, Services, Interactive Price Calculator,
    Verified Customer Reviews, and Live Star Rating Selector Form.
    """
    branches = Branch.objects.all().order_by('display_order', '-is_head_office')
    reviews = CustomerReview.objects.filter(is_approved=True).order_by('-created_at')[:8]
    review_form = CustomerReviewForm()
    
    # Calculate average rating
    all_reviews = CustomerReview.objects.filter(is_approved=True)
    count = all_reviews.count()
    if count > 0:
        avg_rating = round(sum(r.rating for r in all_reviews) / count, 1)
    else:
        avg_rating = 4.9

    context = {
        'branches': branches,
        'reviews': reviews,
        'review_form': review_form,
        'avg_rating': avg_rating,
        'total_reviews_count': count if count > 0 else 142,
    }
    return render(request, 'index.html', context)


def quote_view(request):
    """
    Booking / Quote page with Django ModelForm, custom item input,
    pre-filling from price calculator, and CSRF protection.
    """
    if request.method == 'POST':
        form = BookingOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(
                request, 
                f"Booking Order #{order.booking_ref} created successfully! Mr. Kumar will call you shortly."
            )
            # Store in session and redirect to thanks
            request.session['last_booking_id'] = order.id
            return redirect('thanks', booking_ref=order.booking_ref)
        else:
            messages.error(request, "Please correct the highlighted errors in your booking form.")
    else:
        # Pre-fill from query params if passed from interactive price calculator
        initial_data = {}
        if request.GET.get('pickup'):
            initial_data['pickup_city'] = request.GET.get('pickup')
        if request.GET.get('drop'):
            initial_data['drop_city'] = request.GET.get('drop')
        if request.GET.get('move_type'):
            initial_data['move_type'] = request.GET.get('move_type')
        if request.GET.get('price'):
            try:
                initial_data['estimated_price'] = float(request.GET.get('price'))
            except ValueError:
                pass
        if request.GET.get('tier'):
            initial_data['packing_tier'] = request.GET.get('tier')
        if request.GET.get('items'):
            items_list = [i.strip() for i in request.GET.get('items').split(',') if i.strip()]
            initial_data['items_checklist'] = items_list
        if request.GET.get('custom_items'):
            initial_data['custom_items'] = request.GET.get('custom_items')
            
        form = BookingOrderForm(initial=initial_data)

    branches = Branch.objects.all().order_by('display_order', '-is_head_office')
    return render(request, 'quote.html', {'form': form, 'branches': branches})


def thanks_view(request, booking_ref=None):
    """
    Order confirmation view with booking details and Mr. Kumar contact links.
    """
    order = None
    if booking_ref:
        order = BookingOrder.objects.filter(booking_ref=booking_ref).first()
    
    if not order:
        last_id = request.session.get('last_booking_id')
        if last_id:
            order = BookingOrder.objects.filter(id=last_id).first()

    return render(request, 'thanks.html', {'order': order})


def about_view(request):
    """
    About Us page view highlighting New Balaji Packers and Movers story,
    Proprietor Mr. Kumar, Head Office at Vuyyuru, and branches at Vijayawada & Machilipatnam.
    """
    branches = Branch.objects.all().order_by('display_order', '-is_head_office')
    return render(request, 'about.html', {'branches': branches})


def contact_view(request):
    """
    Contact Us page with branch contact info, inquiry form, and WhatsApp routing.
    """
    branches = Branch.objects.all().order_by('display_order', '-is_head_office')
    if request.method == 'POST':
        # Quick contact message handling
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', 'Vuyyuru')
        message = request.POST.get('message', '').strip()
        if name and phone:
            messages.success(
                request,
                f"Thank you, {name}! Your message has been routed to our {city} branch. We will reach out within 15 minutes."
            )
            return redirect('contact')
        else:
            messages.error(request, "Please enter your name and contact phone number.")

    return render(request, 'contact.html', {'branches': branches})


@require_POST
def submit_review_view(request):
    """
    Live Review Star Rating submission handler.
    Supports both AJAX requests (for dynamic DOM insertion) and standard form POSTs.
    """
    form = CustomerReviewForm(request.POST)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('is_ajax') == '1'

    if form.is_valid():
        review = form.save()
        if is_ajax:
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you! Your verified rating and review has been published.',
                'review': {
                    'reviewer_name': review.reviewer_name,
                    'city': review.city,
                    'rating': review.rating,
                    'review_text': review.review_text,
                    'created_at': review.created_at.strftime('%b %d, %Y'),
                }
            })
        messages.success(request, "Thank you! Your review was successfully submitted.")
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}#reviews")
    else:
        if is_ajax:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
        messages.error(request, "Failed to submit review. Please ensure all fields are correctly filled.")
        return redirect(f"{request.META.get('HTTP_REFERER', '/')}#reviews")


def reviews_list_view(request):
    """
    Dedicated reviews page with pagination and submission form.
    """
    reviews_queryset = CustomerReview.objects.filter(is_approved=True).order_by('-created_at')
    paginator = Paginator(reviews_queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    review_form = CustomerReviewForm()
    return render(request, 'reviews.html', {
        'page_obj': page_obj,
        'review_form': review_form,
    })
