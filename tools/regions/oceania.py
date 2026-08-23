"""
Australasia and the western Pacific, 1886.

Australia is not a country. Federation is fifteen years away, and in 1886 there
are six separate self-governing colonies with their own parliaments, tariffs,
postage and -- famously -- rail gauges, so that trains could not cross the
border between New South Wales and Victoria without passengers changing carriage.
Vanilla draws all of it as one tag; here it is six.

New Guinea is divided three ways in 1884-85 and none of the divisions is
Australian: the Dutch hold the west, Germany the north-east, and Britain the
south-east, the last after Queensland tried to annex it unilaterally in 1883 and
London disallowed it. The Bismarck Archipelago and the northern Solomons are
German from 1884-85.

German colonies go to Prussia, as elsewhere: the Empire's possessions belong to
the Empire, and Prussia stands in for it as the Kaiser's seat.
"""

SPLIT = {
    # ---- the six Australian colonies ----
    "New South Wales":    {"NSW": None},
    "Victoria":           {"VIC": None},
    "Queensland":         {"QLD": None},
    "South Australia":    {"SAS": None},
    "Northern Territory": {"SAS": None},   # administered by South Australia from 1863
    "Central Australia":  {"SAS": None},
    "Western Australia":  {"WAU": None},
    "Tasmania":           {"TAS": None},

    # ---- New Zealand ----
    "Wellington":   {"NZL": None},
    "South Island": {"NZL": None},

    # ---- New Guinea and the Bismarcks, partitioned 1884-85 ----
    "Papua":            {"ENG": None},   # British New Guinea, the south-east
    "Bismarck":         {"PRS": None},   # German New Guinea
    "Solomon Islands":  {"PRS": None},   # the northern Solomons, German from 1885
    "West Papua":       {"HOL": None},   # Dutch since 1828

    # ---- scattered islands ----
    "Ellice Islands": {"ENG": None},
    "Nendo":          {"ENG": None},
    "Aru Islands":    {"HOL": None},
}

NAMES = {
    "NSW": "New South Wales", "VIC": "Victoria", "QLD": "Queensland",
    "SAS": "South Australia", "WAU": "Western Australia", "TAS": "Tasmania",
    "NZL": "New Zealand", "ENG": "United Kingdom", "PRS": "Prussia",
    "HOL": "Netherlands",
}
