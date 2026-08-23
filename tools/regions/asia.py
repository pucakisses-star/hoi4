"""
Asia in 1886: the Qing Empire, Russia east of the Urals, Japan, Korea and
mainland Southeast Asia.

The big correction is the same one the country list makes: CHI is the Republic
of China, and in 1886 there is no republic. The Qing hold everything from the
Amur to Hainan, plus Manchuria, Inner and Outer Mongolia, Tannu Uriankhai,
Xinjiang (made a province in 1884), Taiwan (until 1895), Dalian (until 1898)
and Guangzhouwan (until 1898). All of that is one country.

Other 1886 facts that differ from 1936:

  - Korea is Joseon, independent under Qing suzerainty, not Japanese. Japan
    does not annex it until 1910.
  - Sakhalin is entirely Russian and the Kurils entirely Japanese, under the
    Treaty of Saint Petersburg of 1875.
  - The Philippines, the Carolines, Palau and the Marianas are Spanish. The
    United States does not appear in the Pacific until 1898.
  - The Marshall Islands became a German protectorate in 1885.
  - Cochinchina is a French colony; Annam and Tonkin are a French protectorate
    over the Nguyen empire, which still exists; Cambodia is a French
    protectorate with Norodom still reigning.
  - Laos is not French until 1893. It is two Siamese vassal kingdoms.
  - Tibet is under Qing suzerainty but governs itself, so it keeps its tag.

Several state names in this region are actively wrong -- the source data
localises vanilla state ids using a mod that renumbered them, so state 744 holds
Xian's provinces under the name "Baden". Where that happens the real identity is
noted beside the entry. The provinces are correct; only the labels lie.
"""

_QING_WHOLE = [
    # China proper
    "Beijing", "Hebei", "Shandong", "Henan", "Jiangsu", "Anhui", "Shanghai",
    "Hubei", "Sichuan", "Xikang", "Zhejiang", "Jiangxi", "Hunan", "Guizhou",
    "Fujian", "Shaanxi", "Shanxi", "Suiyuan", "Gansu", "Qinghai", "Alxa",
    "Yunnan", "Guangxi", "Guangdong", "Guangzhou", "Nanning", "Hainan",
    # Manchuria
    "Heilungkiang", "Sungkiang", "Liaoning", "Liaotung", "Kirin", "Jehol",
    # Inner and Outer Mongolia, and Tannu Uriankhai
    "Chahar", "South Chahar", "Mongolia", "Tannu Uriankhai",
    # Xinjiang, a province since 1884
    "Dzungaria", "Urumqi", "Yarkand", "Taklamakan",
]

_RUSSIA_WHOLE = [
    "Northeast Siberia", "Northwest Siberia", "Salekhard", "Okhotsk", "Yeniseisk",
    "Surgut", "Kirensk", "Yakutsk", "Kamchatka", "Tomsk", "Tyumen", "Bodaybo",
    "Bratsk", "Omsk", "Krasnoyarsk", "Novonikolayevsk", "Kemerovo", "Amur",
    "Irkutsk", "Nikolayevsk", "Chita", "Barnaul", "Akmolinsk", "North Sakhalin",
    "Ulan Ude", "Semipalatinsk", "Gorno-Altaysk", "Birobidzhan", "Boli", "Ayaguz",
    "Haishenwai", "Taraz", "Kokand", "Dushanbe",
]

_JAPAN_WHOLE = [
    "Ezo", "Mutsu", "Hokuriku", "Echizen", "Kanto", "Tokai", "Iwami", "Harima",
    "Iyo", "Higo",
    "Okinawa",        # the Ryukyu Kingdom, annexed in 1879
    "Kuril Islands",  # Japanese entire under the 1875 treaty
    "Iwo Jima", "Marcus Island",
]

SPLIT = {}
for _n in _QING_WHOLE:
    SPLIT[_n] = {"QNG": None}
for _n in _RUSSIA_WHOLE:
    SPLIT[_n] = {"RUS": None}
for _n in _JAPAN_WHOLE:
    SPLIT[_n] = {"JAP": None}

SPLIT.update({
    # ---- Qing territory whose state name lies about where it is ----
    "Baden":               {"QNG": None},  # id 744 -- Xian, Shaanxi
    "Roma":                {"QNG": None},  # id 751 -- Liangshan, Sichuan
    "Southern Nile":       {"QNG": None},  # id 752 -- Chamdo
    "Northern Dobrudja":   {"QNG": None},  # id 748 -- Zunyi, Guizhou
    "South Kuril Islands": {"QNG": None},  # id 750 -- Changde, Hunan
    "Suez":                {"QNG": None},  # id 749 -- Huangshan, Anhui
    "Oldenburg":           {"QNG": None},  # id 745 -- Dalian; Russia leases it in 1898
    "Oudh":                {"QNG": None},  # id 756 -- Jiuquan, Gansu
    "Rewa":                {"QNG": None},  # id 755 -- Haixi, Qinghai
    "Gwalior":             {"QNG": None},  # id 754 -- Golog, Qinghai
    "Bikaner":             {"QNG": None},  # id 759 -- Kunlun, Xinjiang
    "Man":                 {"QNG": None},  # id 761 -- Hulunbuir, Manchuria
    "East Hebei":          {"QNG": None},
    "S.W Taiwan":          {"QNG": None},  # Qing until Shimonoseki, 1895
    "Guangzhouwan":        {"QNG": None},  # France does not lease this until 1898

    # ---- Tibet: Qing suzerainty, self-governing ----
    "Tibet":      {"TIB": None},
    "Travancore": {"TIB": None},  # id 758 -- Ngari
    "Malabar":    {"TIB": None},  # id 757 -- Shigatse

    # ---- Korea: Joseon, under Qing suzerainty ----
    "Pyongyang Area": {"KOR": None},
    "South Korea":    {"KOR": None},

    # ---- Sakhalin went to Russia in 1875, the Kurils to Japan ----
    "South Sakhalin": {"RUS": None},

    # ---- Afghanistan under Abdur Rahman Khan ----
    "Kabul": {"AFG": None},
    "Herat": {"AFG": None},

    # ---- Siam, which also holds the northern Malay sultanates as vassals ----
    "Siam":           {"SIA": None},
    "Northern Malay": {"SIA": None},

    # ---- French Indochina as it stood in 1886 ----
    "Tonkin":             {"DNM": None},  # protectorate over the Nguyen empire
    "Southern Indochina": {"FRA": None},  # Cochinchina, an outright colony
    "Cambodia":           {"CAM": None},  # protectorate; Norodom still reigns
    # Laos is Siamese, not French, until 1893: two vassal kingdoms. The
    # Vientiane region, destroyed by Siam in 1828 and administered directly
    # since, is folded into Luang Prabang.
    "Laos": {
        "CPS": [1374, 1520, 1563, 1577, 1592, 4260, 4539, 4554, 7426,
                10195, 10238, 10453, 12210],
        "LUA": None,
    },

    # ---- Spain in the Pacific ----
    "Luzon": {"SPR": None}, "Manila": {"SPR": None}, "Central islands": {"SPR": None},
    "Samar": {"SPR": None}, "Cebu": {"SPR": None}, "Palawan": {"SPR": None},
    "Mindanao": {"SPR": None},
    "Caroline Islands": {"SPR": None}, "Palau": {"SPR": None}, "Saipan": {"SPR": None},

    # ---- Germany's first Pacific protectorate, 1885. The Empire's colonies
    # belong to the Empire; Prussia stands in for it, being where the Kaiser sits.
    "Marshall Islands": {"PRU": None},

    # ---- European possessions already established by 1886 ----
    "Hong Kong":        {"ENG": None},   # ceded 1842
    "Ceylon":           {"ENG": None},
    "Andaman":          {"ENG": None},
    "Maldives":         {"ENG": None},
    "Diego Garcia":     {"ENG": None},
    "Christmas Island": {"ENG": None},
    "Cocos Islands":    {"ENG": None},
    "Fiji":             {"ENG": None},   # annexed 1874
    "Macau":            {"POR": None},
    "Goa":              {"POR": None},
    "Portuguese Timor": {"POR": None},
    "New Caledonia":    {"FRA": None},   # annexed 1853
})

NAMES = {
    "QNG": "Qing Empire", "RUS": "Russian Empire", "JAP": "Japan", "KOR": "Korea",
    "TIB": "Tibet", "AFG": "Afghanistan", "SIA": "Siam", "DNM": "Dai Nam",
    "CAM": "Cambodia", "LUA": "Luang Prabang", "CPS": "Champasak",
    "SPR": "Spain", "PRU": "Prussia", "ENG": "United Kingdom",
    "POR": "Portugal", "FRA": "France",
}
