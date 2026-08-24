"""
India in 1886: the British Raj wrapped around several hundred princely states.

Vanilla draws British India as one country. In 1886 roughly two fifths of the
subcontinent by area was ruled by princes who kept their own courts, armies,
coinage and internal law under British paramountcy, and the largest of them were
the size of European kingdoms -- Hyderabad alone was larger than Italy.

The larger states are separated out here. The many small ones are not: the
province grid cannot carry several hundred polities, and Rajputana alone had
over twenty. Where a vanilla state holds several princely houses the provinces
are divided between the biggest of them by relative position.

A caution on precision. The projection fitted for South Asia is coarse -- 112 km
median residual, the worst of any region so far, because the map distorts badly
here. Absolute coordinates are not trustworthy at that scale, so these splits
use relative position within each state: Bikaner is the north-western corner of
Rajputana, Udaipur the southern, Kutch the north-western corner of Gujarat.
That ordering survives the distortion even where the numbers do not.

Burma is included. Britain annexed it on 1 January 1886, so depending on the
campaign start it is either the last months of the Konbaung dynasty or the first
of a new province.
"""

SPLIT = {
    # ---- states that map cleanly onto one princely house ----
    "Hyderabad": {"HYD": None},
    "Mysore":    {"MYS": None},
    "Indore":    {"INR": None},
    "Kashmir":   {"KSH": None},
    "San Marino": {"KSH": None},   # id 787 -- North Kashmir; the name is wrong
    "Quetta":      {"KLT": None},  # Kalat, under British protection
    "Baluchistan": {"KLT": None},

    # ---- Rajputana, divided between its four largest houses ----
    "Rajahsthan": {
        "BKN": [12876, 12041],                              # Bikaner, the north-west
        "JAI": [2054, 4915, 7905, 7998],                    # Jaipur, the east
        "UDA": [12829, 4149, 4971, 1199, 12743],            # Udaipur (Mewar), the south
        "JOD": None,                                        # Jodhpur (Marwar), the west
    },

    # ---- Gujarat: Kutch, Junagadh, Baroda, and British Surat ----
    "Gujarat": {
        "KTC": [7020, 1061, 1190],                          # Kutch, the north-west
        "JUN": [10118, 12037, 4090, 4132, 7207, 1144],      # Junagadh, in Saurashtra
        "BRD": [12092, 7165, 9975, 11952],                  # Baroda, the east
        "RAJ": None,                                        # British Gujarat and Surat
    },

    # ---- Travancore and Cochin on the Malabar coast ----
    "Madurai": {
        "TRV": [7447, 1238, 1321, 10130, 7288, 10274],
        "CCH": [12275],
        "RAJ": None,                                        # the Madras Presidency
    },

    # ---- directly administered British India ----
    "Punjab": {"RAJ": None}, "Delhi": {"RAJ": None}, "Lucknow": {"RAJ": None},
    "Bihar": {"RAJ": None}, "West Bengal": {"RAJ": None}, "East Bengal": {"RAJ": None},
    "Orissa": {"RAJ": None}, "Assam": {"RAJ": None}, "Arunachal Pradesh": {"RAJ": None},
    "Sind": {"RAJ": None}, "Peshawar": {"RAJ": None}, "Bombay": {"RAJ": None},
    "Madras": {"RAJ": None}, "Jabalpur": {"RAJ": None}, "French India": {"FRA": None},

    # ---- the Himalayan kingdoms ----
    "Nepal":  {"NEP": None},
    "Bhutan": {"BHU": None},

    # ---- Burma, annexed 1 January 1886 ----
    "Burma":    {"BRM": None},
    "Mandalay": {"BRM": None},
}

NAMES = {
    "RAJ": "British India", "HYD": "Hyderabad", "MYS": "Mysore", "INR": "Indore",
    "KSH": "Jammu and Kashmir", "KLT": "Kalat", "BKN": "Bikaner", "JAI": "Jaipur",
    "UDA": "Udaipur", "JOD": "Jodhpur", "KTC": "Kutch", "JUN": "Junagadh",
    "BRD": "Baroda", "TRV": "Travancore", "CCH": "Cochin", "NEP": "Nepal",
    "BHU": "Bhutan", "BRM": "Burma", "FRA": "France",
}
