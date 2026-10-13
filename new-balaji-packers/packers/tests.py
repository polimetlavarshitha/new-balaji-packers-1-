from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from .models import Branch, BookingOrder, CustomerReview
from .forms import BookingOrderForm, CustomerReviewForm


class BranchModelTests(TestCase):
    def test_default_branches_exist(self):
        """Test that the 3 required branches exist with correct details."""
        branches = Branch.objects.all()
        self.assertGreaterEqual(branches.count(), 3)

        vuyyuru = Branch.objects.get(city="Vuyyuru")
        self.assertTrue(vuyyuru.is_head_office)
        self.assertIn("Sai Baba Temple Back Side", vuyyuru.address)
        self.assertEqual(vuyyuru.phone, "9014331173")
        self.assertEqual(vuyyuru.manager_name, "Mr. Kumar")

        vijayawada = Branch.objects.get(city="Vijayawada")
        self.assertFalse(vijayawada.is_head_office)
        self.assertEqual(vijayawada.phone, "9803558899")

        machilipatnam = Branch.objects.get(city="Machilipatnam")
        self.assertFalse(machilipatnam.is_head_office)
        self.assertEqual(machilipatnam.phone, "8099333910")


class BookingOrderTests(TestCase):
    def test_booking_order_creation_and_ref_generation(self):
        """Test creating a booking order generates a unique reference code."""
        order = BookingOrder.objects.create(
            customer_name="Ravi Teja",
            phone="9014331173",
            pickup_city="Vuyyuru",
            drop_city="Vijayawada",
            move_date=date.today() + timedelta(days=5),
            move_type="household",
            custom_items="Heavy wooden showcase, 65-inch curved TV",
            estimated_price=8500.00
        )
        self.assertTrue(order.booking_ref.startswith("NBP-"))
        self.assertEqual(order.status, "Pending")

    def test_booking_order_form_valid(self):
        """Test BookingOrderForm validation with standard and custom items."""
        form_data = {
            'customer_name': 'Naveen Kumar',
            'phone': '9803558899',
            'email': 'naveen@example.com',
            'pickup_city': 'Vuyyuru',
            'drop_city': 'Machilipatnam',
            'move_date': (date.today() + timedelta(days=2)).isoformat(),
            'move_type': 'household',
            'items_checklist': ['Double Bed & Mattress', 'Sofa Set (3+1+1)'],
            'custom_items': 'Temple mandir, 2 Split ACs',
            'packing_tier': 'premium',
            'floor_details': 'Ground to 1st floor',
            'estimated_price': 9200,
            'notes': 'Need morning slot 9 AM',
        }
        form = BookingOrderForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        order = form.save()
        self.assertIn("Double Bed & Mattress", order.selected_items)
        self.assertEqual(order.custom_items, "Temple mandir, 2 Split ACs")

    def test_booking_order_past_date_validation(self):
        """Test that past move dates are rejected."""
        form_data = {
            'customer_name': 'Test User',
            'phone': '9014331173',
            'pickup_city': 'Vuyyuru',
            'drop_city': 'Vijayawada',
            'move_date': (date.today() - timedelta(days=1)).isoformat(),
            'move_type': 'household',
        }
        form = BookingOrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('move_date', form.errors)


class CustomerReviewTests(TestCase):
    def test_customer_review_model_and_ajax_submission(self):
        """Test CustomerReview model and live AJAX submission endpoint."""
        client = Client()
        response = client.post(
            reverse('submit_review'),
            {
                'reviewer_name': 'Anil Kumar',
                'city': 'Vijayawada',
                'rating': '5',
                'review_text': 'Excellent shifting service from Vuyyuru to Vijayawada! On time.',
                'is_ajax': '1',
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['review']['reviewer_name'], 'Anil Kumar')
        self.assertEqual(data['review']['rating'], 5)

        review = CustomerReview.objects.get(reviewer_name='Anil Kumar')
        self.assertEqual(review.city, 'Vijayawada')


class ViewsAndTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_renders_with_branches_and_services(self):
        """Test that the homepage renders 200 with Navy & Amber branding."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "NEW BALAJI")
        self.assertContains(response, "Vuyyuru")
        self.assertContains(response, "Vijayawada")
        self.assertContains(response, "Machilipatnam")
        self.assertContains(response, "Mr. Kumar")
        self.assertContains(response, "9014331173")

    def test_quote_page_get_and_post(self):
        """Test quote page GET and successful booking order submission."""
        response = self.client.get(reverse('quote'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Book Your Relocation Order")
        self.assertContains(response, "Custom &amp; Extra Item Input")

        post_data = {
            'customer_name': 'K. Prasad',
            'phone': '8099333910',
            'pickup_city': 'Machilipatnam',
            'drop_city': 'Vijayawada',
            'move_date': (date.today() + timedelta(days=3)).isoformat(),
            'move_type': 'household',
            'custom_items': 'Bicycle, 5 storage trunks',
            'packing_tier': 'premium',
            'estimated_price': 7800,
        }
        post_response = self.client.post(reverse('quote'), post_data)
        # Should redirect to thanks page
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(post_response.url.startswith('/thanks/'))

    def test_about_and_contact_pages(self):
        """Test about and contact pages load with branch details."""
        about_res = self.client.get(reverse('about'))
        self.assertEqual(about_res.status_code, 200)
        self.assertContains(about_res, "About New Balaji Packers and Movers")

        contact_res = self.client.get(reverse('contact'))
        self.assertEqual(contact_res.status_code, 200)
        self.assertContains(contact_res, "9014331173")
        self.assertContains(contact_res, "9803558899")
        self.assertContains(contact_res, "8099333910")
