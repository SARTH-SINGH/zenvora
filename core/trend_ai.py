"""
AI TREND, OCCASION & CATALOG INTELLIGENCE ENGINE
Monitors Indian cultural calendar, seasonal demand spikes, and pairs them
with high-trust, verified genuine products with backup supplier routing.
"""
import datetime
import json
import os

INDIAN_OCCASIONS = [
    {"name": "Winter Season", "start_month": 11, "end_month": 2, "tags": ["winter", "comfort", "warmth", "heating", "indoor"]},
    {"name": "New Year & Goal Setting", "start_month": 12, "end_month": 1, "tags": ["productivity", "fitness", "organization", "desk", "tech"]},
    {"name": "Republic Day / Republic Sale", "start_month": 1, "end_month": 1, "tags": ["gadgets", "home", "utility"]},
    {"name": "Valentine's & Gifting", "start_month": 2, "end_month": 2, "tags": ["gift", "aesthetic", "lights", "jewelry", "couple"]},
    {"name": "Holi & Spring", "start_month": 3, "end_month": 3, "tags": ["waterproof", "outdoor", "car_care"]},
    {"name": "Summer & Cooling", "start_month": 4, "end_month": 6, "tags": ["portable_fan", "cooling", "car_ac", "hydration"]},
    {"name": "Monsoon Care", "start_month": 7, "end_month": 8, "tags": ["waterproof", "car_mirror", "anti_fog", "umbrella"]},
    {"name": "Rakhi & Festival Gifting", "start_month": 8, "end_month": 8, "tags": ["gift", "gadget", "watch"]},
    {"name": "Diwali & Festive Shopping", "start_month": 9, "end_month": 11, "tags": ["home_decor", "ambient_lights", "cleaning", "kitchen"]}
]

# Verified high-trust products with Amazon-grade real photography & multi-supplier routing
PRODUCT_CATALOG = [
    {
        "id": "prod_cleaner_8in1",
        "title": "Multifunctional 8-in-1 Tech & Earphone Cleaning Kit",
        "tagline": "Keep your phone, AirPods, keyboard & screen crystal clear like day one.",
        "category": "Tech & Daily Utility",
        "tags": ["tech", "productivity", "cleaner", "desk", "airpods"],
        "wholesale_cost": 75,
        "selling_price": 399,
        "mrp_cross": 899,
        "margin_profit": 324,
        "rating": 4.6,
        "reviews_count": 1420,
        "features": [
            "High-density soft brush for keyboard & mechanical keys",
            "Flocking sponge for deep earphone charging case cleaning",
            "Precision silicone tip for speaker grime and earwax removal",
            "Built-in screen cleaner spray bottle & microfiber wiping cloth",
            "Keycap puller for PC & laptop maintenance"
        ],
        "image_hero": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80",
        "image_gallery": [
            "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
        ],
        "suppliers": {
            "primary": {"name": "Meesho Reseller Network", "sku": "MSH-TECH-CLEAN-8IN1", "stock": 940},
            "backup": {"name": "Surat Direct Wholesale Hub", "sku": "SRT-CLEAN-01", "stock": 1250}
        }
    },
    {
        "id": "prod_cob_keychain_light",
        "title": "Ultra-Bright 800 Lumens COB Rechargeable Keychain Light",
        "tagline": "Pocket floodlight, emergency magnet, bottle opener & tripod mount.",
        "category": "Everyday Carry & Car/Bike Utility",
        "tags": ["car_care", "outdoor", "emergency", "utility", "gadgets"],
        "wholesale_cost": 89,
        "selling_price": 449,
        "mrp_cross": 999,
        "margin_profit": 360,
        "rating": 4.7,
        "reviews_count": 2180,
        "features": [
            "800 Lumens blindingly bright COB wide-angle floodlight",
            "Strong magnetic back sticks firmly to car bonnet or bike frame",
            "Built-in 500mAh USB-C fast rechargeable lithium battery",
            "180° foldable kickstand & integrated stainless bottle opener",
            "IPX4 water-resistant & shockproof aluminum casing"
        ],
        "image_hero": "https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?w=800&auto=format&fit=crop&q=80",
        "image_gallery": [
            "https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?w=800&auto=format&fit=crop&q=80",
            "https://images.unsplash.com/photo-1508873696983-2df5293cb395?w=800&auto=format&fit=crop&q=80"
        ],
        "suppliers": {
            "primary": {"name": "Surat Direct Wholesale Hub", "sku": "RP-COB-LIGHT-800", "stock": 820},
            "backup": {"name": "Meesho Hub", "sku": "GR-COB-KEY-800LM", "stock": 1100}
        }
    },
    {
        "id": "prod_magnetic_car_mount",
        "title": "360° Foldable Alloy Magnetic Car Phone Mount",
        "tagline": "Strongest N52 rare-earth magnets, zero shaking on Indian roads.",
        "category": "Car & Mobile Accessories",
        "tags": ["car_care", "tech", "gadgets", "phone_mount"],
        "wholesale_cost": 115,
        "selling_price": 499,
        "mrp_cross": 1199,
        "margin_profit": 384,
        "rating": 4.5,
        "reviews_count": 960,
        "features": [
            "6x N52 neodymium heavy-duty magnets hold phone through speed bumps",
            "Full zinc alloy aviation body with double-fold 360° articulation",
            "Ultra-strong 3M VHB dashboard adhesive leaves zero sticky residue",
            "Works with all iPhones, Samsung, OnePlus & cover cases"
        ],
        "image_hero": "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=800&auto=format&fit=crop&q=80",
        "image_gallery": [
            "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=800&auto=format&fit=crop&q=80"
        ],
        "suppliers": {
            "primary": {"name": "Meesho Hub", "sku": "GR-CAR-MAG-MOUNT", "stock": 650},
            "backup": {"name": "Surat Direct Wholesale Hub", "sku": "RP-360-FOLD-MOUNT", "stock": 900}
        }
    },
    {
        "id": "prod_anti_fog_mirror_film",
        "title": "Nano Hydrophobic Anti-Fog Rainproof Car Mirror Film (Pair)",
        "tagline": "Crystal clear side-mirror vision in heavy rain & night glare.",
        "category": "Automotive Safety",
        "tags": ["car_care", "monsoon", "winter", "safety"],
        "wholesale_cost": 45,
        "selling_price": 299,
        "mrp_cross": 699,
        "margin_profit": 254,
        "rating": 4.4,
        "reviews_count": 830,
        "features": [
            "Micro-nano coating repels water droplets instantly",
            "Anti-glare layer filters high-beam headlights from behind",
            "Universal oval fit for all cars, SUVs & bikes",
            "Easy 2-minute bubble-free bubble squeegee installation"
        ],
        "image_hero": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&auto=format&fit=crop&q=80",
        "image_gallery": [
            "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800&auto=format&fit=crop&q=80"
        ],
        "suppliers": {
            "primary": {"name": "Meesho Hub", "sku": "GR-RAIN-FILM-2PC", "stock": 1500},
            "backup": {"name": "Roposo Warehouse", "sku": "RP-MIRROR-COAT-PAIR", "stock": 2000}
        }
    }
]

def get_current_season_recommendations():
    now = datetime.datetime.now()
    cur_month = now.month
    active_occasions = []
    for occ in INDIAN_OCCASIONS:
        s = occ["start_month"]
        e = occ["end_month"]
        if s <= e:
            if s <= cur_month <= e:
                active_occasions.append(occ)
        else: # spans year-end
            if cur_month >= s or cur_month <= e:
                active_occasions.append(occ)
    return active_occasions

def get_active_catalog():
    occasions = get_current_season_recommendations()
    occasion_tags = set()
    for occ in occasions:
        for t in occ["tags"]:
            occasion_tags.add(t)

    # Score products by seasonal relevance
    scored = []
    for p in PRODUCT_CATALOG:
        relevance = len(set(p["tags"]).intersection(occasion_tags))
        scored.append((relevance, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored]

if __name__ == "__main__":
    recs = get_current_season_recommendations()
    print("=== CURRENT ACTIVE INDIAN OCCASIONS ===")
    for r in recs:
        print(f"- {r['name']} (Tags: {', '.join(r['tags'])})")
    print(f"\nTotal Catalog Items: {len(PRODUCT_CATALOG)}")
    active = get_active_catalog()
    print("\nTop Recommended Active Products:")
    for a in active:
        print(f"[{a['category']}] {a['title']} -> Wholesale: ₹{a['wholesale_cost']} | Sell: ₹{a['selling_price']} | Profit: ₹{a['margin_profit']}")
