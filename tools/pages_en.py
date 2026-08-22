# -*- coding: utf-8 -*-
"""English page bodies — assembled from tools/en/*.py, same keys as pages.PAGES.

Output goes to site/en/<same filename>.html so relative links between pages keep
working; asset paths are prefixed with ../ by build.py. The admin panel is
Turkish-only and has no English page.
"""

from en.part1 import INDEX, SAHIPLEN, GECICI_YUVA, SAHIPLENMEDEN_ONCE, SAHIPLENME_SURECI
from en.part2 import (BAGIS_YAP, KORUYUCU_MELEK, E_KARTLAR, KURTARAN_SHOP,
                      GUNCEL_IHTIYACLAR, GONULLU_OL, KURUMSAL)
from en.part3 import HIKAYEMIZ, ETKIMIZ, YASAM_ALANLARI, HIKAYELER, ILETISIM
from en.part4 import katalog, ILAN_DETAY

PAGES_EN = {
    "index.html": {
        "title": "Kurtaran Ev | A safe life for every animal",
        "description": "Kurtaran Ev rescues, treats and rehomes more than 1,500 cats and dogs "
                       "across four shelters in Istanbul.",
        "body": INDEX,
        "veri": True,
        "js": ["assets/js/counts.js"],
    },
    "sahiplen.html": {
        "title": "Adopt | Kurtaran Ev",
        "description": "Meet the cats and dogs looking for a home and learn how adoption works.",
        "body": SAHIPLEN,
        "veri": True,
        "js": ["assets/js/counts.js"],
    },
    "gecici-yuva.html": {
        "title": "Foster | Kurtaran Ev",
        "description": "Become a foster home; one kennel frees up, one more life is rescued.",
        "body": GECICI_YUVA,
    },
    "sahiplenmeden-once.html": {
        "title": "Before You Adopt | Kurtaran Ev",
        "description": "What to know before adopting: preparation, budget, home safety and expectations.",
        "body": SAHIPLENMEDEN_ONCE,
    },
    "sahiplenme-sureci.html": {
        "title": "Adoption Process | Kurtaran Ev",
        "description": "How the adoption process works and which documents are needed.",
        "body": SAHIPLENME_SURECI,
    },
    "bagis-yap.html": {
        "title": "Donate | Kurtaran Ev",
        "description": "Your donation goes directly to food, treatment and running the shelters.",
        "body": BAGIS_YAP,
    },
    "koruyucu-melek.html": {
        "title": "Guardian Angel | Kurtaran Ev",
        "description": "Keep care going with regular monthly support.",
        "body": KORUYUCU_MELEK,
    },
    "e-kartlar.html": {
        "title": "E-cards & Certificates | Kurtaran Ev",
        "description": "Turn your donation into a personalised e-card or certificate.",
        "body": E_KARTLAR,
    },
    "kurtaran-shop.html": {
        "title": "Kurtaran Shop | Kurtaran Ev",
        "description": "Every purchase from Kurtaran Shop goes straight to the field.",
        "body": KURTARAN_SHOP,
    },
    "guncel-ihtiyaclar.html": {
        "title": "Current Needs | Kurtaran Ev",
        "description": "This week's priority food, litter and medical supply needs at our shelters.",
        "body": GUNCEL_IHTIYACLAR,
    },
    "gonullu-ol.html": {
        "title": "Volunteer | Kurtaran Ev",
        "description": "In the field, online or in the office — contribute your skills to Kurtaran Ev.",
        "body": GONULLU_OL,
    },
    "kurumsal-is-birligi.html": {
        "title": "Corporate Partnerships | Kurtaran Ev",
        "description": "Project sponsorship, corporate Guardian Angel and employee volunteering models.",
        "body": KURUMSAL,
    },
    "hikayemiz.html": {
        "title": "Our Story & Mission | Kurtaran Ev",
        "description": "How Kurtaran Ev started, what it believes in and what it does.",
        "body": HIKAYEMIZ,
    },
    "etkimiz.html": {
        "title": "Our Impact & Work | Kurtaran Ev",
        "description": "Kurtaran Ev in numbers; our areas of work and goals for the coming period.",
        "body": ETKIMIZ,
    },
    "yasam-alanlari.html": {
        "title": "Visit Our Shelters | Kurtaran Ev",
        "description": "Hadımköy, the Cat Shelter, Beşiktaş and Dumankaya: four shelters and how to visit.",
        "body": YASAM_ALANLARI,
    },
    "hikayeler.html": {
        "title": "News & Stories | Kurtaran Ev",
        "description": "Happy endings, notes from the field and news from our projects.",
        "body": HIKAYELER,
    },
    "iletisim.html": {
        "title": "Contact | Kurtaran Ev",
        "description": "Get in touch with Kurtaran Ev about adoption, donations, volunteering and partnerships.",
        "body": ILETISIM,
    },

    # --- listing catalogue ---------------------------------------------------
    "yuva-arayan-kopekler.html": {
        "title": "Dogs Looking for a Home | Kurtaran Ev",
        "description": "Browse the dogs waiting for adoption, filtered by age, size and compatibility.",
        "body": katalog("kopek"),
        "veri": True,
        "js": ["assets/js/catalog.js"],
    },
    "yuva-arayan-kediler.html": {
        "title": "Cats Looking for a Home | Kurtaran Ev",
        "description": "Browse the cats waiting for adoption, filtered by age, sex and compatibility.",
        "body": katalog("kedi"),
        "veri": True,
        "js": ["assets/js/catalog.js"],
    },
    "ilan.html": {
        "title": "Listing | Kurtaran Ev",
        "description": "Listing details for an animal looking for a home.",
        "body": ILAN_DETAY,
        "veri": True,
        "js": ["assets/js/animal.js"],
    },
}
