from .models import Branch


def business_context(request):
    """
    Context processor to provide business info and branches to all templates.
    """
    branches = Branch.objects.all().order_by('display_order', '-is_head_office')
    
    services = [
        {
            "title": "Household Articles Shifting",
            "desc": "Complete home relocation with high-grade bubble wrap, carton packing, careful loading, and uninstallation/re-installation.",
            "icon": "bi-house-heart",
            "emoji": "🏠",
            "tag": "Most Popular"
        },
        {
            "title": "Office Relocation & IT Assets",
            "desc": "Zero-downtime commercial shifting for workstations, IT servers, modular office furniture, and sensitive document archives.",
            "icon": "bi-building",
            "emoji": "🏢",
            "tag": "Corporate"
        },
        {
            "title": "Car & Bike Transportation",
            "desc": "Specialized open and closed container car carriers and bike crates with door-to-door tracking and full transit insurance coverage.",
            "icon": "bi-truck",
            "emoji": "🚗",
            "tag": "Dedicated Carrier"
        },
        {
            "title": "Packing & Unpacking Services",
            "desc": "Expert multi-layer packaging using 5-ply corrugated sheets, thermocol, air bubble roll, stretch film, and heavy-duty tape.",
            "icon": "bi-box-seam",
            "emoji": "📦",
            "tag": "Damage-Free"
        },
        {
            "title": "Local & All India Intercity Moving",
            "desc": "Daily scheduled transport between Vuyyuru, Vijayawada, Machilipatnam, Hyderabad, Bangalore, Chennai, and all Indian cities.",
            "icon": "bi-geo-alt",
            "emoji": "🚚",
            "tag": "All India"
        },
    ]

    return {
        "BUSINESS_NAME": "New Balaji Packers and Movers",
        "PROPRIETOR": "Mr. Kumar",
        "TAGLINE": "Safe Move ... Happy Home | Your Trust, Our Responsibility",
        "PRIMARY_PHONE": "9014331173",
        "ALL_PHONES": ["9014331173", "9803558899", "8099333910"],
        "WHATSAPP_LINK": "https://wa.me/919014331173?text=Hello%20Mr.%20Kumar%20(New%20Balaji%20Packers%20and%20Movers),%20I%20would%20like%20to%20get%20a%20quote%20for%20relocation.",
        "ALL_BRANCHES": branches,
        "SERVICES_LIST": services,
        "HEAD_OFFICE_CITY": "Vuyyuru",
        "HEAD_OFFICE_ADDRESS": "Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru",
    }
