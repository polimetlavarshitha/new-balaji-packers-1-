# New Balaji Packers and Movers - Django Web Application

Complete production-ready Django project for **New Balaji Packers and Movers** adhering to the MVT architecture, Bootstrap 5 responsive UI, interactive JavaScript components, and Render cloud deployment files.

---

## 🏢 Business Information
- **Business Name:** New Balaji Packers and Movers
- **Proprietor:** Mr. Kumar
- **Tagline:** Safe Move ... Happy Home | Your Trust, Our Responsibility
- **Head Office / Main Branch:** Vuyyuru (Thotlavallaru Road, Sai Baba Temple Back Side) | 📞 9014331173
- **Branch 2:** Vijayawada (Opp. Nagarjuna Hospital, Kanuru, Auto Nagar, Vijayawada) | 📞 9803558899
- **Branch 3:** Machilipatnam (Housing Board Colony, Bypass Road, Machilipatnam) | 📞 8099333910
- **Official Bills:** GST Invoices Available | Bank Approval Bills Available
- **Payment Modes:** PhonePe, Google Pay, Paytm, UPI, Direct Bank Transfer

---

## 🏗️ Architecture & Features

### 1. Django MVT Architecture (3 Models)
- **`Branch`**: Manages hub locations, designating Vuyyuru as Head Office / Main Branch with badge tagging, addresses, contact phones, and manager info.
- **`BookingOrder`**: Manages relocation quote bookings with auto-generated reference codes (`NBP-YYYYMMDD-XXXXXX`), route, schedule, standard item checklists, custom items, packing quality, and estimated price.
- **`CustomerReview`**: Manages verified customer ratings (1 to 5 stars) and review feedback.

### 2. Django ModelForm with CSRF & Custom Item Input
- **`BookingOrderForm`**: Full ModelForm supporting standard furniture checklists and **dedicated custom item input** (e.g., piano, gym equipment, fragile artifacts, extra ACs) with CSRF protection (`{% csrf_token %}`) and phone/date validation.
- **`CustomerReviewForm`**: ModelForm for submitting customer feedback and star ratings.

### 3. Bootstrap 5 Navy Blue & Amber Theme
- High-contrast, modern UI built on Bootstrap 5.3 + custom theme tokens:
  - Deep Navy Blue (`#070e1e` / `#0a192f` / `#0f172a` / `#1e293b`)
  - Vibrant Amber Gold (`#f59e0b` / `#fbbf24` / `#d97706`)
- Fully responsive across desktop, tablet, and mobile devices.

### 4. 2 Interactive JavaScript Features
1. **Interactive Price Calculator (`static/js/calculator.js`)**:
   - Real-time reactive price estimator based on distance matrix (Vuyyuru ↔ Vijayawada ↔ Machilipatnam ↔ Intercity), home size (1 BHK to Villa), packing grade (Standard, Premium Bubble-Wrap, Heavy-Duty Wooden Crate), floor level/stair surcharges, and item toggles.
   - Live breakdown of Freight, Packaging, and Labor fees.
   - **"Apply Estimate & Book Order"** button that pre-populates the Booking Form with the calculated estimate!
2. **Live Review Star Rating Selector (`static/js/reviews.js`)**:
   - 5-star interactive rating widget with gold hover illumination and click-locking.
   - Dynamic live sentiment label (*1 Star: Needs Improvement* → *5 Stars: Outstanding! Highly Recommended!*).
   - Seamless AJAX form submission that prepends the new review into the feed without page reloads.

### 5. Render Deployment Files
- `requirements.txt`: Django, Gunicorn, WhiteNoise, dj-database-url, python-dotenv.
- `render.yaml`: Complete Render Blueprint service definition.
- `build.sh`: Automated executable build script.
- `Procfile`: `web: gunicorn balaji_packers.wsgi:application`.
- `create_superuser.py`: Auto-initializes Django superuser and ensures branch seed records.
- `settings.py`: Production settings with WhiteNoise compressed staticfiles and database URL fallback.

---

## 🚀 Running Locally

1. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
   *(Initial Branch records for Vuyyuru, Vijayawada, Machilipatnam and initial reviews are automatically seeded via data migration `0002_populate_branches`)*

4. **Initialize Superuser & Admin:**
   ```bash
   python create_superuser.py
   ```
   *Default Admin Credentials:*
   - **Username:** `admin`
   - **Password:** `admin123`
   - **Email:** `admin@balajipackers.com`

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Access website at: **http://127.0.0.1:8000/**  
   Access Admin Portal at: **http://127.0.0.1:8000/admin/**

---

## 🧪 Running Tests

Execute the automated test suite:
```bash
python manage.py test
```
All 8 test cases verify models, forms, custom item inputs, view routing, and AJAX review submission.
