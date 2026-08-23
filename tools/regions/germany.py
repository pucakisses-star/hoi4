"""
Germany 1886 -- the German Empire's twenty-six member states.

In 1886 the Empire is twenty-six states that kept their own crowns, armies and
postal services until 1918. Vanilla draws that ground as twenty-four states
belonging to one country, so most of them have to be cut.

Every province was placed by converting its centroid to latitude and longitude
and comparing against where the 1886 border ran. Where a fragment is small the
note records the town it stands for, so the choice can be checked.
"""

SPLIT = {
    "Schleswig": {
        "PRU": [11251, 11366, 317, 6389, 3231, 6257, 3368, 9320],
        "HAM": [9347],    # Hamburg, free city
        "LUB": [11331],   # Lubeck, free city
        "OLD": [13664],   # Principality of Lubeck (Eutin) -- Oldenburg exclave
    },
    "East Prussia":      {"PRU": [395, 6332, 3384, 6402, 9327, 266, 11245, 9398,
                                  3380, 11386, 3351, 6375, 9372, 9346]},
    "Eastern Pomerania": {"PRU": [11343, 11372, 11316, 9361, 9334, 11288, 6334,
                                  9306, 9277, 11260, 6309, 6282, 6390, 9252]},
    "Pomerania":         {"PRU": [9388, 3340, 349, 3258, 3312, 3207]},
    "Ostmark":           {"PRU": [9387, 6236, 537, 11478, 3473, 444, 3572]},
    "Rhineland":         {"PRU": [3512, 3444, 6469, 9482, 6570, 587, 9522, 529, 3547]},
    "Lower Silesia":     {"PRU": [3438, 9470, 3510, 6595, 3283, 552, 6462, 11517,
                                  6534, 9570, 3545, 3485]},
    "Upper Silesia":     {"PRU": [479, 9511, 506, 6512, 11467, 9457, 13663]},
    "Posen":             {"PRU": [11232, 388, 3381, 6558, 17, 3532, 9532, 3460, 11558]},
    "Pomerellen":        {"PRU": [9263, 362, 389, 334, 3324, 6347, 3295, 279, 243]},
    "Alsace-Lorraine":   {"ALS": [11531, 9559, 11502, 549, 3629, 1346, 9503, 6529, 678]},
    "Lower Bavaria":     {"BAV": [586, 3571, 571, 11497, 3541, 3299, 532, 9515, 9681, 6725]},
    "Upper Bavaria":     {"BAV": [6540, 3705, 708, 11653, 3688, 692, 9666, 6693,
                                  9652, 707, 11620, 11638]},
    "Brandenburg": {
        "PRU": [11219, 3367, 11444, 375, 11359, 11505, 13497, 6521, 9496, 9456,
                3522, 3499, 9428, 11415, 478],
        "ANH": [6487, 9560],   # Anhalt: Bernburg and Dessau, enclaved in Prussian Saxony
    },
    "Mecklenburg-Schwerin": {
        "MKS": [9294, 11305, 11276, 321, 293],
        "MKT": [268],          # Mecklenburg-Strelitz, around Neustrelitz
    },
    "Hannover": {
        "PRU": [374, 6349, 6325, 3326, 6298, 9264, 3271, 6263, 9238, 6218,
                6377, 3395, 9375, 11493, 6513, 11402],
        "BRU": [526, 11468],   # Brunswick proper, and the Blankenburg exclave
    },
    "Saxony": {
        "SXY": [573, 11481, 6559, 9471, 9441],   # the Kingdom: Dresden, Leipzig, Bautzen, Zwickau
        "PRU": [6441, 11545, 9535, 3535, 514, 3514],  # Prussian Saxony and Lusatia
    },
    "Weser-Ems": {
        "PRU": [11360, 13839, 11264, 3234, 247, 9281, 11233, 11388],  # East Frisia, Emsland, Osnabruck
        "OLD": [241, 13562, 336],   # Oldenburg proper
        "BRE": [309],               # Bremen, free city
    },
    "Westphalia": {
        "PRU": [11346, 9509, 6622, 6535, 11431, 495, 3398],
        "SLP": [405],    # Schaumburg-Lippe, Buckeburg
        "LIP": [3355],   # Lippe, Detmold
        "WLD": [9443],   # Waldeck-Pyrmont, Arolsen
    },
    "Eastern Hesse": {
        "PRU": [564, 13665, 9524, 11533, 3524, 9547, 11445, 3397, 6488, 6444],
        "HES": [9486, 589, 11560, 6549],  # Grand Duchy: Darmstadt, Mainz, Worms, Upper Hesse
        "BDN": [3574],                    # Baden's northern Odenwald
    },
    "Franken": {
        "BAV": [3474, 11404, 11417, 6594, 9416, 9572, 9557, 11544, 11529, 561],
        "SMN": [13116],  # Saxe-Meiningen's southern territory
        "SCG": [6421],   # Coburg -- the other half of Saxe-Coburg-Gotha
    },
    "Palatinate": {
        "PRU": [13448, 11494, 11470, 11435, 9575],  # Prussian Rhine Province
        "BAV": [3558, 563, 11547],                  # the Rhenish Palatinate, detached from Bavaria
        "OLD": [3423],                              # Birkenfeld, Oldenburg exclave on the Nahe
    },
    "Wurttemberg": {
        "WUR": [6581, 6555, 9545, 519, 11499, 3690, 694, 11486, 9655],
        "BDN": [6568, 3530, 6542, 6712, 3692, 3679, 11640],  # the Rhine strip: Karlsruhe to Konstanz
        "PRU": [9517, 6934],   # Hohenzollern, the dynasty's ancestral land, ruled from Berlin
    },
    # Ten provinces, eight sovereign states and Prussian Erfurt. Each duchy gets
    # the province standing closest to its capital. The real duchies were
    # interleaved with dozens of exclaves; no grid at this resolution reproduces
    # that, and this does not pretend to.
    "Thuringia": {
        "WEI": [6524],   # Saxe-Weimar-Eisenach   -- Weimar, 8 km
        "SCG": [13408],  # Saxe-Coburg-Gotha      -- Gotha, 6 km
        "SMN": [482],    # Saxe-Meiningen         -- Meiningen
        "SAT": [6501],   # Saxe-Altenburg         -- Altenburg
        "REU": [9497],   # Reuss Elder Line       -- Greiz
        "RYL": [538],    # Reuss Younger Line     -- Gera
        "SWS": [3500],   # Schwarzburg-Sondershausen
        "SWR": [425],    # Schwarzburg-Rudolstadt -- its northern block
        "PRU": [3561, 6582],  # the Harz, and Halle in Prussian Saxony
    },
}

NAMES = {
    "PRU": "Prussia", "BAV": "Bavaria", "SXY": "Saxony", "WUR": "Wurttemberg",
    "BDN": "Baden", "HES": "Hesse", "MKS": "Mecklenburg-Schwerin",
    "MKT": "Mecklenburg-Strelitz", "OLD": "Oldenburg", "BRU": "Brunswick",
    "WEI": "Saxe-Weimar-Eisenach", "SMN": "Saxe-Meiningen", "SAT": "Saxe-Altenburg",
    "SCG": "Saxe-Coburg and Gotha", "ANH": "Anhalt", "SWR": "Schwarzburg-Rudolstadt",
    "SWS": "Schwarzburg-Sondershausen", "WLD": "Waldeck-Pyrmont",
    "REU": "Reuss Elder Line", "RYL": "Reuss Younger Line",
    "SLP": "Schaumburg-Lippe", "LIP": "Lippe", "LUB": "Lubeck", "BRE": "Bremen",
    "HAM": "Hamburg", "ALS": "Alsace-Lorraine",
}


