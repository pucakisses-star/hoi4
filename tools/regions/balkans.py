"""
Austria-Hungary and the Balkans, 1886.

The region vanilla draws for 1936 barely resembles 1886. Yugoslavia and
Czechoslovakia do not exist; their ground is Habsburg or Ottoman. The Ottoman
Empire still holds Kosovo, Macedonia, Albania, Epirus and Thrace in Europe.
Bosnia is Ottoman in law and Austro-Hungarian in fact, occupied since 1878 and
not annexed until 1908. Bessarabia is Russian, taken back from Romania in 1878.

Borders used, all as they stood in 1886:
  - Serbia's 1878 frontier, south to roughly the latitude of Vranje. Kosovo,
    the Sandzak of Novi Pazar and everything below stayed Ottoman until 1912.
  - Montenegro's post-1878 borders, with Niksic, Podgorica and Kolasin gained
    at Berlin but Bijelo Polje and Pljevlja still Ottoman.
  - Greece's 1881 frontier, which brought in Thessaly and Arta. Ioannina and
    Epirus remained Ottoman until 1913.
  - Bulgaria including Eastern Rumelia, seized in September 1885 and accepted
    by the Porte at Tophane in April 1886, but not the Rhodope and Kardzhali
    strip, which stayed Ottoman.
  - The Prut as the Romania-Russia border, and Northern Dobruja Romanian,
    both from the 1878 settlement.
"""

SPLIT = {
    # ---- Cisleithania: the Austrian half ----
    "Upper Austria":     {"AUS": None},
    "Lower Austria":     {"AUS": None},
    "Tyrol":             {"AUS": None},
    "Bohemia":           {"AUS": None},
    "Sudetenland":       {"AUS": None},
    "Moravia":           {"AUS": None},
    "Moravian Silesia":  {"AUS": None},
    "Olsagebiet":        {"AUS": None},
    "West Galicia":      {"AUS": None},
    "East Galicia":      {"AUS": None},
    "South Galicia":     {"AUS": None},
    "Bukowina":          {"AUS": None},
    "Carniola":          {"AUS": None},
    "Istria":            {"AUS": None},   # the Austrian Littoral
    "North Dalmatia":    {"AUS": None},   # Kingdom of Dalmatia
    "Zara":              {"AUS": None},

    # ---- Transleithania: the Hungarian half ----
    "Transdanubia":          {"HUN": None},
    "Great Hungarian Plain": {"HUN": None},
    "North Hungary":         {"HUN": None},
    "Upper Hungary":         {"HUN": None},
    "West Slovakia":         {"HUN": None},
    "East Slovakia":         {"HUN": None},
    "Subcarpathia":          {"HUN": None},
    "North Transylvania":    {"HUN": None},
    "South Transylvania":    {"HUN": None},
    "Kreischgebiet":         {"HUN": None},
    "East Banat":            {"HUN": None},
    "West Banat":            {"HUN": None},
    "Vojvodina":             {"HUN": None},
    "Slavonia":              {"CRO": None},   # Croatia-Slavonia, autonomous under Hungary

    # ---- occupied Bosnia, and the Croatian bank of the Sava ----
    "West Bosnia": {
        "CRO": [6614, 6619, 13880],   # north of the Sava: the old Military Frontier
        "BOS": [11574, 9588, 9591, 13879, 9586, 606, 6983, 13878, 6799, 11572,
                3985, 13877, 9922, 11741, 13876, 11872, 6957, 11899, 6942,
                13874, 13875, 13781, 13873, 953, 982, 13852, 9894, 11845,
                13779, 13872],
    },

    # ---- Serbia, and the Ottoman ground below it ----
    "Morava": {
        "SER": [6634, 630, 13675, 9756, 9602, 6998, 6970, 11887, 3939, 13851,
                11868, 6953, 9906, 13855, 13850, 11857, 13854],
        "OTT": [3922, 6940, 9849, 9874, 13864, 11832, 9890],  # Kosovo and the Sandzak
    },
    "Belgrade": {"SER": None},

    # ---- Montenegro, the Sandzak, and Pec ----
    "Ipek": {
        "MTN": [9821, 13778, 9809, 11858, 13780],  # Niksic, Cetinje, Podgorica, Kolasin
        "OTT": [13776, 13777, 13775, 6913],        # Bijelo Polje, Pljevlja, Pec
        "SER": [937],                              # Uzice
    },

    # ---- Bulgaria with Eastern Rumelia, less the Ottoman Rhodopes ----
    "Tarevo": {
        "BUL": [3796, 9610, 6842, 3952, 3819, 13863, 13862, 6982, 6952, 6814,
                3937, 6923, 11813],
        "OTT": [9818, 13856, 893, 878, 13858, 9862, 13857],  # Rhodope and Kardzhali
    },
    "Sofia":             {"BUL": None},
    "Varna":             {"BUL": None},
    "Southern Dobrudja": {"BUL": None},   # Romania took only the northern half in 1878

    # ---- Romania, and Russian Bessarabia ----
    "Muntenia": {"ROM": None},
    "Oltenia":  {"ROM": None},
    "Moldova": {
        "ROM": [3407, 13678, 11534, 6584, 6761, 11689, 744, 9716, 3728, 3741,
                711, 6747, 11672, 3689, 6729, 11655, 9701, 6706, 11652],
        "RUS": [723, 3724],                     # east of the Prut
    },
    "Bessarabia": {"RUS": None},                # returned to Russia at Berlin, 1878
    "Koinadugu": {                              # misnamed in the source data: this is the Budjak
        "RUS": [6743, 13679, 6727, 13680, 3704, 13682, 3701],
        "ROM": [687],                           # the Danube delta, Northern Dobruja
    },

    # ---- Greece after 1881, and Ottoman Epirus ----
    "Northern Greece": {
        "GRE": [11786, 9916, 11895, 12001, 1205, 1106],       # Thessaly and Arta
        "OTT": [9837, 6900, 3448, 841, 3980, 914, 3914, 9805],  # Epirus and Ioannina
    },
    "Central Greece": {"GRE": None},
    "Peloponnese":    {"GRE": None},
    "Aegean Islands": {"GRE": None},
    "Chania":         {"CRT": None},   # Crete, autonomous under the Pact of Halepa

    # ---- Ottoman Rumelia ----
    "Macedonia":          {"OTT": None},
    "Southern Macedonia": {"OTT": None},
    "Albania":            {"OTT": None},
    "Thrace":             {"OTT": None},
    "Adrianople":         {"OTT": None},
    "Dodecanese":         {"OTT": None},   # Italy does not take these until 1912
}

NAMES = {
    "AUS": "Austria", "HUN": "Hungary", "CRO": "Croatia-Slavonia",
    "BOS": "Bosnia and Herzegovina", "SER": "Serbia", "MTN": "Montenegro",
    "BUL": "Bulgaria", "ROM": "Romania", "GRE": "Greece", "OTT": "Ottoman Empire",
    "CRT": "Crete", "RUS": "Russian Empire",
}
