"""
The Near East, 1886: Ottoman Asia, Persia, Egypt, the Mahdist Sudan and Arabia.

The correction this region exists to make: Russia took Kars, Ardahan and Batumi
from the Ottomans at the Congress of Berlin in 1878 and held them until 1918.
An earlier pass left the whole of Anatolia Ottoman because the Central European
projection is unreliable that far east and guessing the salient would have been
worse than deferring it. Fitted on thirty Near Eastern anchors instead, the
provinces of that salient are identifiable and are carved out here.

Other things that are 1886 rather than 1936:

  - Syria, Palestine and Transjordan are Ottoman provinces. There are no
    mandates until after 1918; an earlier pass had put Mount Lebanon under
    France thirty-four years early.
  - Mount Lebanon is an autonomous mutasarrifate with a Christian governor
    guaranteed by the powers after the 1860 massacres, so it keeps its own tag.
  - Egypt is a Khedivate under Ottoman suzerainty, occupied by Britain since
    1882 but not annexed. It is Egyptian, not British.
  - Sudan is not Egyptian at all. The Mahdists took Khartoum in January 1885
    and killed Gordon; they hold it until Omdurman in 1898.
  - Central Arabia belongs to the Rashidi of Ha'il, not the Saudis. The Second
    Saudi State is a rump that is extinguished outright in 1891.
  - Yemen is the Ottoman Yemen Vilayet. Aden has been British since 1839.
"""

SPLIT = {
    # ---- Anatolia ----
    "Kastamonu": {"OTT": None}, "Izmit":   {"OTT": None}, "Samsun":  {"OTT": None},
    "Bursa":     {"OTT": None}, "Angora":  {"OTT": None}, "Sivas":   {"OTT": None},
    "Kayseri":   {"OTT": None}, "Afyon":   {"OTT": None}, "Smyrna":  {"OTT": None},
    "Konya":     {"OTT": None}, "Malatya": {"OTT": None}, "Adana":   {"OTT": None},
    "Adalia":    {"OTT": None}, "Mersin":  {"OTT": None}, "Van":     {"OTT": None},

    # the 1878 Russian salient: Batumi on the coast, Artvin inland, Ardahan
    "Trabzon": {"RUS": [7454, 10403, 10472], "OTT": None},
    # Kars and Kagizman
    "Erzurum": {"RUS": [4583, 12376], "OTT": None},

    # ---- Ottoman Syria, and autonomous Mount Lebanon ----
    "Damascus":  {"OTT": None},
    "Palestine": {"OTT": None},
    "Jordan":    {"OTT": None},
    "Lebanon":   {"MLB": None},   # the Mount Lebanon Mutasarrifate

    # ---- Ottoman Mesopotamia ----
    "Mosul":      {"OTT": None},
    "Baghdad":    {"OTT": None},
    "Al Hajara":  {"OTT": None},

    # ---- Egypt: Ottoman in law, British-occupied since 1882, Egyptian in fact ----
    "Cairo":          {"EGY": None},
    "Alexandria":     {"EGY": None},
    "Sinai":          {"EGY": None},
    "Eastern Desert": {"EGY": None},
    "Aswan":          {"EGY": None},

    # ---- the Mahdist state ----
    "Khartoum": {"MHD": None},

    # ---- Persia ----
    "Tibriz":    {"PER": None}, "Gilan":     {"PER": None}, "Tehran":  {"PER": None},
    "Khorasan":  {"PER": None}, "Semnan":    {"PER": None}, "Hamadan": {"PER": None},
    "Kurdistan": {"PER": None}, "Isfahan":   {"PER": None}, "Kerman":  {"PER": None},
    "Khuzestan": {"PER": None}, "Fars":      {"PER": None}, "Sistan":  {"PER": None},

    # ---- Arabia ----
    "Hejaz":        {"HEJ": None},   # Ottoman vilayet under the Sharif of Mecca
    "Ha'il":        {"RSD": None},   # Jabal Shammar: the Rashidi, the real power here
    "Rub al Khali": {"NEJ": None},   # what is left of the Second Saudi State
    "Kuwait":       {"KUW": None},   # Ottoman kaza under the Al-Sabah
    "Abu Dhabi":    {"TRU": None},   # the Trucial States
    "Muscat":       {"OMA": None},
    "Yemen":        {"OTT": None},   # the Ottoman Yemen Vilayet
    "Aden":         {"ENG": None},   # British since 1839
}

NAMES = {
    "OTT": "Ottoman Empire", "RUS": "Russian Empire", "MLB": "Mount Lebanon",
    "EGY": "Egypt", "MHD": "Mahdist State", "PER": "Persia", "HEJ": "Hejaz",
    "RSD": "Jabal Shammar", "NEJ": "Nejd", "KUW": "Kuwait",
    "TRU": "Trucial States", "OMA": "Oman", "ENG": "United Kingdom",
}
