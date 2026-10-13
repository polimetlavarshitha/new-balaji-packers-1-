import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'balaji-packers-secret-key-2026'
    
    # Proprietor Info
    PROPRIETOR = "Mr. Kumar"
    TAGLINE = "Safe Move ... Happy Home | Your Trust, Our Responsibility"
    
    # Official Phone Numbers
    PHONES = ["9014331173", "9803558899", "8099333910"]
    
    # Official Branch Details (Vuyyuru set as Main Head Office)
    BRANCHES = [
        {
            "city": "Vuyyuru",
            "is_main": True,
            "badge": "Head Office / Main Branch",
            "address": "Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru",
            "phone": "9014331173"
        },
        {
            "city": "Vijayawada",
            "is_main": False,
            "badge": "Branch Office",
            "address": "Opp. Nagarjuna Hospital, Kanuru, Auto Nagar, Vijayawada",
            "phone": "9803558899"
        },
        {
            "city": "Machilipatnam",
            "is_main": False,
            "badge": "Branch Office",
            "address": "Housing Board Colony, Bypass Road, Machilipatnam",
            "phone": "8099333910"
        }
    ]
    
    # Services List
    SERVICES = [
        ("Packing & Loading", "Careful packing with bubble wrap and sturdy boxes.", "📦"),
        ("Household Articles Shifting", "Complete home shifting service across all locations.", "🏠"),
        ("Office Relocation", "Safe moving of furniture, computers, and files.", "🏢"),
        ("Car Transportation", "Secure vehicle carrier transport across India.", "🚗"),
        ("Local & Intercity Moving", "Fast, reliable transportation on time.", "🚚")
    ]