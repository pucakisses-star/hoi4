"""
Insular Southeast Asia, 1886: the Dutch East Indies, the Malay sultanates and
British Borneo.

Vanilla draws the archipelago as eight enormous states under one Dutch tag and
the peninsula as two under one Malayan tag. In 1886 neither is a country. The
Dutch hold Java and the coasts and are thirteen years into a war with Aceh that
has another eighteen to run; Bali is five kingdoms; every Malay state is
separately sovereign under its own sultan; and Borneo is split between a Sultan
of Brunei, an English dynasty ruling Sarawak as rajahs, and a chartered company.

Only the states with a real 1886 identity are separated out. The Dutch keep
everything they actually administered.
"""

SPLIT = {
    "Sumatra": {
        "ACE": [7658, 10509, 13768, 12488, 1648],   # Aceh, at war with the Dutch since 1873
        "DLI": [4652, 13767],                       # Deli, the tobacco plantation belt
        "SKI": [7463, 12168, 1277],                 # Siak
        "HOL": None,
    },
    "Java":       {"HOL": None},
    "Kalimantan": {"HOL": None},
    "West Papua": {"HOL": None},
    "Aru Islands": {"HOL": None},

    "Sulawesi": {
        "BNE": [1589, 13753, 10263, 4349],          # Bone, the Bugis kingdom
        "HOL": None,
    },
    "The Moluccas": {
        "TRN": [1419, 10141, 7413],                 # Ternate
        "TID": [1437],                              # Tidore
        "HOL": None,
    },
    "Lesser Sunda Islands": {
        "BLL": [13752, 13751, 13750],               # Buleleng, northern Bali
        "KLU": [13749],                             # Klungkung, nominal overlord of Bali
        "BDG": [13747],                             # Badung, southern Bali
        "LOM": [13748, 7293],                       # Lombok, Balinese-ruled over a Sasak population
        "HOL": None,
    },

    # ---- the Malay peninsula: every state separately sovereign ----
    "Malacca": {
        "KED": [12144],                             # Kedah, under Siamese suzerainty
        "KEL": [7329],                              # Kelantan, likewise
        "TRG": [12199],                             # Terengganu, likewise
        "PRK": [4310, 7342, 1364, 10227, 12215],    # Perak, the tin state
        "SEL": [4384, 1376],                        # Selangor
        "NSN": [12255, 10297, 12271],               # Negeri Sembilan
        "PHG": [4355, 1348, 7399, 1392],            # Pahang
        "JOH": [4412, 4367, 7427, 4424],            # Johor, fully sovereign under Abu Bakar
        "HOL": [12113],                             # Riau, Dutch
        "ENG": None,                                # the Straits Settlements
    },

    # ---- Borneo, divided three ways ----
    "North Borneo": {
        "NBO": [4282, 10143, 10212, 10199, 12186, 1306, 10240, 12171],
        "BRN": [7371, 7387],                        # what is left of Brunei
        "SRW": [10285, 10269, 8091, 4396, 12283, 2117, 7443, 4216, 12905, 1208],
        "HOL": None,                                # Dutch Borneo
    },
}

NAMES = {
    "HOL": "Netherlands", "ACE": "Aceh", "DLI": "Deli", "SKI": "Siak",
    "BNE": "Bone", "TRN": "Ternate", "TID": "Tidore", "BLL": "Buleleng",
    "KLU": "Klungkung", "BDG": "Badung", "LOM": "Lombok", "KED": "Kedah",
    "KEL": "Kelantan", "TRG": "Terengganu", "PRK": "Perak", "SEL": "Selangor",
    "NSN": "Negeri Sembilan", "PHG": "Pahang", "JOH": "Johor",
    "ENG": "United Kingdom", "NBO": "North Borneo", "BRN": "Brunei",
    "SRW": "Sarawak",
}
