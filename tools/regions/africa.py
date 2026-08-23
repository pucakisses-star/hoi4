"""
Africa, 1886 -- the year after the Berlin Conference, when the partition was
agreed on paper and had barely begun on the ground.

This is where the 1936 map is least like 1886, and where vanilla is most
misleading. Italy does not hold Libya until 1911; Belgium does not hold the
Congo until 1908; Britain does not hold Kenya, Uganda, Tanganyika or Rhodesia
at all yet. Assigning any of those to their 1936 owner puts a colony on the map
twenty-five years early.

The recovered geometry already carries a good deal of African work from the
previous mod -- Ashanti, Dahomey, the Mossi, the Aro, the Kru, Wadai, the
Sotho, the Orange Free State and others exist as tags with territory. That is
1886-appropriate and is kept. What is corrected here is the colonial layer
sitting on top of it.
"""

SPLIT = {
    # ---- North Africa ----
    # Libya is Ottoman. Italy invades in 1911, twenty-five years after this.
    "Tripoli": {"OTT": None}, "Tripolitania": {"OTT": None}, "Sirte": {"OTT": None},
    "Benghasi": {"OTT": None}, "Cyrenaica": {"OTT": None}, "Derna": {"OTT": None},
    "El Agheila": {"OTT": None}, "Libyan Desert": {"OTT": None},

    "Tunisia": {"TUN": None},   # a French protectorate from 1881, the Bey still reigning
    "Gabes":   {"TUN": None},
    "Tlemcen":         {"FRA": None},   # Algeria, French since 1830
    "Algerian Desert": {"FRA": None},
    "North Morocco": {"MOR": None},     # an independent sultanate until 1912
    "South Morocco": {"MOR": None},
    "Rio de Oro":     {"SPR": None},
    "Canary islands": {"SPR": None},
    "Marsa Matruh":   {"EGY": None},
    "Western Desert": {"EGY": None},
    "Sudan": {"MHD": None},             # the Mahdists, not Britain, until 1898

    # ---- West Africa ----
    "Senegal":         {"FRA": None},
    "Mali":            {"FRA": None},
    "Southern Sahara": {"FRA": None},
    "Ivory Coast":     {"FRA": None},
    "Gabon":           {"FRA": None},
    "Waddai":          {"WDD": None},   # the Sultanate of Wadai
    "Nigeria":         {"SOK": None},   # the Sokoto Caliphate, the largest state in Africa
    "Ghana":           {"ASH": None},   # Ashanti, independent until 1902
    "Gambia":          {"ENG": None},
    "Sierra Leone":    {"ENG": None},
    "Portuguese Guinea": {"POR": None},
    "Cape Verde":      {"POR": None},
    "Sao Tome":        {"POR": None},
    "Madeira":         {"POR": None},
    "Equatorial Guinea": {"SPR": None},

    # ---- Central Africa ----
    # The Congo Free State: Leopold II's personal property, recognised at
    # Berlin in 1885. It does not become Belgian until 1908.
    "Northern Congo": {"CFS": None},
    "Central Congo":  {"CFS": None},
    "Ndkala":         {"CFS": None},
    "Central Africa": {"WDD": None},

    # ---- East Africa ----
    "Tanganyika": {"PRS": None},   # German East Africa, chartered 1885
    "Uganda":     {"BUG": None},   # the Kingdom of Buganda under Mwanga II
    "Kenya":      {"ZAN": None},   # the Sultan of Zanzibar's mainland coast
    "Ankole":     {"NKO": None},
    "Oromia":     {"ETH": None},
    "Eritrea":    {"ITA": None},   # Italy took Massawa in 1885
    "Somaliland": {"MJT": None},   # the Majeerteen Sultanate; Italy arrives in 1889
    "Warsangeli": {"MJT": None},
    "Djibouti":   {"FRA": None},   # Obock, French since 1862
    "Madagascar": {"MER": None},   # the Merina kingdom, under French protectorate from Dec 1885
    "Comoro Islands": {"FRA": None},
    "Seychelles": {"ENG": None}, "Mauritius": {"ENG": None},
    "Reunion": {"FRA": None},

    # ---- Southern Africa ----
    "Namibian Desert": {"PRS": None},   # German South West Africa, 1884
    "Pretoria":        {"TVL": None},   # the South African Republic
    "Cape":            {"ENG": None},
    "Natal":           {"ENG": None},
    "Rhodesia":        {"MTB": None},   # Lobengula's Ndebele kingdom; Rhodes arrives in 1890
    "Bechuanaland":    {"BCH": None},
    "Thaba Bosiu":     {"BSU": None},
    "Basutoland":      {"BSU": None},
    "Angola":          {"POR": None},
    "Mozambique":      {"POR": None},

    # ---- Atlantic and Indian Ocean specks ----
    "Ascension": {"ENG": None}, "Saint Helena": {"ENG": None},
    "Kerguelen": {"FRA": None},
}

NAMES = {
    "OTT": "Ottoman Empire", "TUN": "Tunisia", "FRA": "France", "MOR": "Morocco",
    "SPR": "Spain", "EGY": "Egypt", "MHD": "Mahdist State", "WDD": "Wadai",
    "SOK": "Sokoto Caliphate", "ASH": "Ashanti", "ENG": "United Kingdom",
    "POR": "Portugal", "CFS": "Congo Free State", "PRS": "Prussia",
    "BUG": "Buganda", "ZAN": "Zanzibar", "NKO": "Nkore", "ETH": "Ethiopia",
    "ITA": "Italy", "MJT": "Majeerteen", "MER": "Merina", "TVL": "South African Republic",
    "MTB": "Matabeleland", "BCH": "Bechuanaland", "BSU": "Basutoland",
}
