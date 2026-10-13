from django.db import migrations


def seed_branches_and_reviews(apps, schema_editor):
    Branch = apps.get_model('packers', 'Branch')
    CustomerReview = apps.get_model('packers', 'CustomerReview')

    branches_data = [
        {
            "city": "Vuyyuru",
            "is_head_office": True,
            "badge_text": "Head Office / Main Branch",
            "address": "Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru",
            "phone": "9014331173",
            "alt_phone": "9803558899",
            "manager_name": "Mr. Kumar",
            "landmark": "Sai Baba Temple Back Side",
            "display_order": 1,
            "service_hours": "24/7 Available (All India Moving)",
        },
        {
            "city": "Vijayawada",
            "is_head_office": False,
            "badge_text": "Branch Office",
            "address": "Opp. Nagarjuna Hospital, Kanuru, Auto Nagar, Vijayawada",
            "phone": "9803558899",
            "alt_phone": "9014331173",
            "manager_name": "Mr. Kumar",
            "landmark": "Opp. Nagarjuna Hospital, Kanuru",
            "display_order": 2,
            "service_hours": "24/7 Available",
        },
        {
            "city": "Machilipatnam",
            "is_head_office": False,
            "badge_text": "Branch Office",
            "address": "Housing Board Colony, Bypass Road, Machilipatnam",
            "phone": "8099333910",
            "alt_phone": "9014331173",
            "manager_name": "Mr. Kumar",
            "landmark": "Housing Board Colony, Bypass Road",
            "display_order": 3,
            "service_hours": "24/7 Available",
        },
    ]

    for b in branches_data:
        Branch.objects.update_or_create(
            city=b["city"],
            defaults=b
        )

    reviews_data = [
        {
            "reviewer_name": "Ramesh V.",
            "city": "Vijayawada",
            "rating": 5,
            "review_text": "Shifted our 3 BHK house from Vuyyuru Main Branch to Vijayawada seamlessly. Mr. Kumar's team handled all fragile glassware and electronics with multi-layer bubble wrap. Extremely satisfied!",
            "is_approved": True,
        },
        {
            "reviewer_name": "Priya M.",
            "city": "Machilipatnam",
            "rating": 5,
            "review_text": "Very safe packing and secure transportation for our office equipment in Machilipatnam. Delivered right on time with GST invoice for company reimbursement.",
            "is_approved": True,
        },
        {
            "reviewer_name": "Venkateswara Rao",
            "city": "Vuyyuru",
            "rating": 5,
            "review_text": "Best packers and movers in Krishna district. Their team at Thotlavallaru Road (Sai Baba temple back side) was punctual, courteous, and extremely professional.",
            "is_approved": True,
        },
        {
            "reviewer_name": "Suresh Babu K.",
            "city": "Vijayawada",
            "rating": 5,
            "review_text": "Relocated our household goods and two-wheeler from Vijayawada to Hyderabad. Zero scratches, loaded carefully, and delivered in 24 hours. Highly recommended!",
            "is_approved": True,
        },
    ]

    for r in reviews_data:
        CustomerReview.objects.get_or_create(
            reviewer_name=r["reviewer_name"],
            city=r["city"],
            defaults=r
        )


def reverse_seed(apps, schema_editor):
    Branch = apps.get_model('packers', 'Branch')
    CustomerReview = apps.get_model('packers', 'CustomerReview')
    Branch.objects.filter(city__in=["Vuyyuru", "Vijayawada", "Machilipatnam"]).delete()
    CustomerReview.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('packers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_branches_and_reviews, reverse_seed),
    ]
