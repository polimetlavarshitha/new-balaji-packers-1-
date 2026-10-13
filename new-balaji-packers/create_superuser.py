"""
create_superuser.py
Deployment & local script to create Django superuser and ensure branch records exist.
Can be executed as: python create_superuser.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'balaji_packers.settings')
django.setup()

from django.contrib.auth import get_user_model
from packers.models import Branch, CustomerReview

User = get_user_model()


def main():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@balajipackers.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

    print(f"[*] Checking Django superuser: {username}")
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    
    user.email = email
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    if created:
        print(f"[+] Superuser '{username}' created successfully!")
    else:
        print(f"[+] Superuser '{username}' password and permissions updated successfully!")

    print("[*] Verifying Branch records...")
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
        branch_obj, b_created = Branch.objects.update_or_create(
            city=b["city"],
            defaults=b
        )
        status = "Created" if b_created else "Updated"
        print(f"  - [{status}] {branch_obj.city}: {branch_obj.badge_text} ({branch_obj.phone})")

    print("[OK] Initialization complete. Admin access ready: Username='admin', Password='(configured)'")


if __name__ == '__main__':
    main()
