"""
The tail: states already sitting on a correct 1886 owner, plus four that are not.

Most of these are West African polities the previous mod had already built --
the Kong empire, the Toucouleur, the Kru, the Mossi, the Aro, Dahomey, Liberia,
the Orange Free State. They were already right for 1886 and are stamped here so
the coverage figure counts what was actually checked rather than what merely
looked plausible.

Four were wrong and are corrected:

  Guam          Spanish until 1898, not American.
  Setsoto       in Basutoland, not French. The name is a Sotho place name and
                the previous data had it under France.
  Anziku        a Congo kingdom, inside the Congo Free State, not Spanish.
  Port-de-Paix  in Haiti, not Spanish. Spain's half of Hispaniola had been the
                Dominican Republic since 1865.
"""

SPLIT = {
    # ---- already correct, stamped after checking ----
    "Bloemfontein": {"OFS": None}, "Vrede": {"OFS": None},
    "Adam Kok se Land": {"OFS": None}, "Winburg": {"OFS": None},
    "Senari":        {"KOG": None},   # the Kong empire
    "Mauritania":    {"TRZ": None},   # the Toucouleur empire
    "Kru":           {"KRU": None},
    "Wilno":         {"RUS": None},   # Vilnius, Russian
    "Bombali":       {"MNH": None}, "Guinea": {"MNH": None},
    "Northern Mali": {"TUG": None},
    "Aro":           {"ARO": None}, "West Aro": {"ARO": None}, "Opobo": {"ARO": None},
    "Togo":          {"DAH": None}, "Benin": {"DAH": None},
    "Burkina Faso":  {"MOS": None},   # the Mossi kingdoms
    "Kailahun":      {"KOY": None},
    "Bong":          {"MND": None},
    "Niger":         {"DDI": None},
    "Liberia":       {"LIB": None},
    "Gilbert Islands": {"ENG": None}, "Nauru": {"ENG": None},
    "Wake Island":   {"USA": None}, "Attu Island": {"USA": None},

    # ---- corrected ----
    "Guam":         {"SPR": None},   # Spanish until 1898
    "Setsoto":      {"BSU": None},   # Basutoland, not France
    "Anziku":       {"CFS": None},   # a Congo kingdom, not Spain
    "Port-de-Paix": {"HAI": None},   # Haiti, not Spain
}

NAMES = {
    "OFS": "Orange Free State", "KOG": "Kong", "TRZ": "Toucouleur", "KRU": "Kru",
    "RUS": "Russian Empire", "MNH": "Mandinka", "TUG": "Tuareg", "ARO": "Aro",
    "DAH": "Dahomey", "MOS": "Mossi", "KOY": "Koya", "MND": "Mande", "DDI": "Zarma",
    "LIB": "Liberia", "ENG": "United Kingdom", "USA": "United States",
    "SPR": "Spain", "BSU": "Basutoland", "CFS": "Congo Free State", "HAI": "Haiti",
}
