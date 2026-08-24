#!/usr/bin/env python3
"""
countries_1886.py -- the 1886 world, restricted to polities Hearts of Iron IV
does not model.

HOI4 ships roughly 190 country tags for a 1936 world. Fifty years earlier the
map is a different object: the German Empire is 25 states that kept their own
crowns, India is a British administration wrapped around several hundred
princely states, West Africa is a dozen sovereign empires, and southern Africa
is two Boer republics plus a scatter of African kingdoms. None of that exists
in the base game.

Each row is a polity that (a) existed during 1886 and (b) has no vanilla HOI4
equivalent. Countries the base game already covers -- Ethiopia, Liberia, Nepal,
Bhutan, Siam, Persia, Afghanistan, Oman, Yemen, Korea, Mongolia, Tibet, Morocco
and the Latin American republics -- are deliberately absent; they need no new
tag. A short list of judgement calls is at the bottom of this file.

Fields: tag, name, region, status in 1886, note.

    python3 tools/countries_1886.py --check     validate tags only
    python3 tools/countries_1886.py --write     emit mod files + reference doc
"""

import argparse
import collections
import os
import sys

# Vanilla HOI4 tags. Used only to refuse a collision, so it errs on the side of
# listing more rather than fewer. Anything here is a tag we must not claim.
def _tags_in_use(path="tools/data/state_geometry.tsv"):
    """Tags already used as a state owner in the recovered geometry.

    This was originally a hand-written list of vanilla tags, and it was wrong:
    it missed 26 tags actually in use, including PRU, which vanilla uses for
    Peru. Prussia was assigned PRU on the strength of that list and collided
    with five Peruvian states. Read the data instead of trusting a list.
    """
    out = set()
    try:
        with open(path, encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                if i == 0:
                    continue
                f = line.rstrip("\n").split("\t")
                if len(f) > 4 and f[4].strip():
                    out.add(f[4].strip())
    except FileNotFoundError:
        pass
    return out


VANILLA = _tags_in_use() | set("""
AFG ALB ANG ARG AST AUS BEL BHU BLR BOL BRA BUL CAN CGX CHI CHL COL COS CRO CUB
CYP CZE DEN DOM ECU EGY ENG EST ETH FIN FRA GER GRE GUA GXC HAI HOL HON HUN ICE
IND INS IRE IRQ ITA JAP KOR LAT LEB LIB LIT LUX MAL MAN MEN MEX MON MOR MTN NEP
NIC NOR NZL OMA PAK PAL PAN PAR PER PHI POL POR PRC PRU RAJ ROM SAF SAL SAU SER
SIA SIK SLO SOV SPA SPD SPR SWE SWI SYR THA TIB TUR URG USA VEN VIN XSA XSM YEM
YUG ZIM D01 D02 D03 D04 D05 D06 D07 D08 D09 D10 D11 D12 D13 D14 D15
""".split())

# tag  name  region  status  note
ROWS = [
# ---- German Empire: sovereign states that kept their monarchs until 1918 ----
("PRS","Prussia","German Empire","Kingdom, hegemon of the Empire","Two thirds of the Empire's territory and population; its king is the Kaiser."),
("BAV","Bavaria","German Empire","Kingdom","Ludwig II is deposed and dies in June 1886. Kept its own army, railways and diplomatic corps."),
("SXY","Saxony","German Empire","Kingdom","Third largest German state; the Empire's industrial heart after Prussia."),
("WUR","Wurttemberg","German Empire","Kingdom","Retained its own army corps and postal service."),
("BDN","Baden","German Empire","Grand Duchy","Liberal constitution; Friedrich I."),
("HES","Hesse","German Empire","Grand Duchy","Hesse-Darmstadt; the northern half was annexed by Prussia in 1866."),
("MKS","Mecklenburg-Schwerin","German Empire","Grand Duchy","Still governed under the 1755 feudal constitution -- the most reactionary state in the Empire."),
("MKT","Mecklenburg-Strelitz","German Empire","Grand Duchy","Tiny partner duchy to Schwerin."),
("OLD","Oldenburg","German Empire","Grand Duchy","Includes the exclaves of Birkenfeld and Lubeck-Eutin."),
("BRU","Brunswick","German Empire","Duchy, in regency","The Guelph claimant is barred by Prussia; ruled by a regent from 1885."),
("WEI","Saxe-Weimar-Eisenach","German Empire","Grand Duchy","The Ernestine senior line; Weimar's cultural prestige far exceeds its size."),
("SMN","Saxe-Meiningen","German Empire","Duchy","Home of the Meiningen court theatre."),
("SAT","Saxe-Altenburg","German Empire","Duchy",""),
("SCG","Saxe-Coburg and Gotha","German Empire","Duchy","Dynastically tied to Britain, Belgium and Portugal."),
("ANH","Anhalt","German Empire","Duchy",""),
("SWR","Schwarzburg-Rudolstadt","German Empire","Principality",""),
("SWS","Schwarzburg-Sondershausen","German Empire","Principality",""),
("WLD","Waldeck-Pyrmont","German Empire","Principality","Administered by Prussia under treaty since 1867 but still formally sovereign."),
("REU","Reuss Elder Line","German Empire","Principality","Every male ruler of both Reuss lines is named Heinrich."),
("RYL","Reuss Younger Line","German Empire","Principality",""),
("SLP","Schaumburg-Lippe","German Empire","Principality",""),
("LIP","Lippe","German Empire","Principality","Its 1895 succession dispute nearly split the Empire's federal council."),
("LUB","Lubeck","German Empire","Free City","Hanseatic republic."),
("BRE","Bremen","German Empire","Free City","Hanseatic republic; Germany's second port."),
("HAM","Hamburg","German Empire","Free City","Hanseatic republic; joined the customs union only in 1888."),
("ALS","Alsace-Lorraine","German Empire","Imperial Territory","Taken in 1871, ruled directly from Berlin with no vote in the federal council."),

# ---- Australasia: six separate self-governing colonies until 1901 ----
("NSW","New South Wales","Australasia","Self-governing British colony","Federation is fifteen years away; in 1886 these six are separate colonies with their own parliaments, tariffs and even rail gauges."),
("VIC","Victoria","Australasia","Self-governing British colony","The gold colony; richer and more populous than New South Wales in this decade."),
("QLD","Queensland","Australasia","Self-governing British colony","Annexed south-eastern New Guinea in 1883 on its own initiative, which London disallowed."),
("SAS","South Australia","Australasia","Self-governing British colony","Administers the Northern Territory from 1863."),
("WAU","Western Australia","Australasia","Crown colony","Does not get responsible government until 1890."),
("TAS","Tasmania","Australasia","Self-governing British colony",""),

# ---- Eastern Europe ----
("RUS","Russian Empire","Eastern Europe","Empire","SOV is the Soviet Union: different state, different borders, no Finland, no Poland, no Bessarabia, and a Tsar rather than a Politburo."),

# ---- Habsburg lands and the Balkans ----
("BOS","Bosnia and Herzegovina","Balkans","Ottoman de jure, Austro-Hungarian occupation","Occupied since 1878; annexed outright only in 1908."),
("ERU","Eastern Rumelia","Balkans","Autonomous Ottoman province, seized by Bulgaria","Bulgaria annexed it in September 1885; the powers had not accepted this in 1886."),
("CRT","Crete","Balkans","Autonomous Ottoman province","Christian governor under the 1878 Pact of Halepa; in near-permanent revolt."),
("SMO","Samos","Balkans","Autonomous Ottoman principality","Ruled by a Christian prince appointed from Constantinople."),

# ---- Ottoman Empire and its autonomous fringe ----
("OTT","Ottoman Empire","Near East","Empire","HOI4's TUR is the post-1923 republic -- a different state with different borders, subjects and institutions."),
("TUN","Tunisia","North Africa","French protectorate","The Bey still reigns; France took the protectorate in 1881. Not a vanilla tag despite appearances, so it has to be defined here."),
("TRP","Tripolitania","North Africa","Ottoman vilayet","The last Ottoman holding in Africa; Italy takes it in 1911."),
("MLB","Mount Lebanon","Near East","Autonomous Ottoman mutasarrifate","Christian governor guaranteed by the powers after the 1860 massacres."),

# ---- Arabia and the Gulf ----
("HEJ","Hejaz","Arabia","Ottoman vilayet under the Sharif of Mecca","Custodian of Mecca and Medina."),
("NEJ","Emirate of Nejd","Arabia","Collapsing Saudi state","The Second Saudi State, reduced to a Rashidi dependency; extinguished in 1891."),
("RSD","Jabal Shammar","Arabia","Emirate","The Rashidi state at Ha'il -- the dominant power in central Arabia in 1886, not the Saudis."),
("ASR","Asir","Arabia","Ottoman-claimed highland emirate",""),
("KUW","Kuwait","Arabia","Ottoman kaza under the Al-Sabah","British protectorate from 1899."),
("BHR","Bahrain","Arabia","British protectorate","Under the 1880 exclusive agreement."),
("QAT","Qatar","Arabia","Ottoman kaza under the Al-Thani",""),
("TRU","Trucial States","Arabia","British-protected sheikhdoms","Abu Dhabi, Dubai, Sharjah and the rest; the later UAE."),
("ZAN","Zanzibar","East Africa","Sultanate","Split from Oman in 1856; controls the Swahili coast and the clove and slave trades."),

# ---- Central Asia ----
("KHI","Khiva","Central Asia","Russian protectorate","Khanate, vassal since 1873."),
("BUK","Bukhara","Central Asia","Russian protectorate","Emirate, vassal since 1868."),

# ---- India: the larger princely states ----
("HYD","Hyderabad","India","Princely state, British paramountcy","The largest and richest: a Muslim Nizam over a mostly Hindu population."),
("MYS","Mysore","India","Princely state","Restored to the Wadiyars in 1881 after fifty years of direct British rule."),
("BRD","Baroda","India","Princely state","Ruled by the Gaekwads."),
("GWA","Gwalior","India","Princely state","Ruled by the Scindias, the strongest of the old Maratha houses."),
("INR","Indore","India","Princely state","Ruled by the Holkars."),
("TRV","Travancore","India","Princely state","Among the most literate and administratively advanced states in India."),
("CCH","Cochin","India","Princely state",""),
("KSH","Jammu and Kashmir","India","Princely state","Dogra dynasty; the frontier of the Great Game."),
("JAI","Jaipur","India","Princely state","Rajputana."),
("JOD","Jodhpur","India","Princely state","Marwar; the largest Rajput state by area."),
("UDA","Udaipur","India","Princely state","Mewar; the senior Rajput house, which never gave a daughter to the Mughals."),
("BKN","Bikaner","India","Princely state","Rajputana."),
("BHP","Bhopal","India","Princely state","Ruled 1844-1926 by a succession of women, the Begums of Bhopal."),
("PTL","Patiala","India","Princely state","The premier Sikh state."),
("REW","Rewa","India","Princely state","Central India."),
("JUN","Junagadh","India","Princely state","Kathiawar."),
("KTC","Kutch","India","Princely state",""),
("BWP","Bahawalpur","India","Princely state","Punjab."),
("KLT","Kalat","India","Khanate under British protection","Baluchistan."),
("MNP","Manipur","India","Princely state","Annexed in 1891 after the Anglo-Manipur War."),
("SKM","Sikkim","India","Himalayan protectorate","British protectorate confirmed in 1890."),

# ---- Southeast Asia ----
("BRM","Burma","Southeast Asia","Konbaung kingdom, annexed 1 January 1886","The Third Anglo-Burmese War ends and Thibaw is exiled -- the kingdom dies in the mod's first days."),
("DNM","Dai Nam","Southeast Asia","Nguyen empire under French protectorate","Annam and Tonkin became protectorates in 1884; Cochinchina is an outright colony."),
("CAM","Cambodia","Southeast Asia","French protectorate","Norodom I; the 1884 convention stripped most royal power."),
("LUA","Luang Prabang","Southeast Asia","Lao kingdom, Siamese vassal","Passes to France in 1893."),
("CPS","Champasak","Southeast Asia","Lao kingdom, Siamese vassal",""),
("JOH","Johor","Southeast Asia","Independent sultanate","The last Malay state to keep full sovereignty; Abu Bakar is treated as an equal in London."),
("PRK","Perak","Southeast Asia","British-resident sultanate","Tin wealth; the Residency system began here in 1874."),
("SEL","Selangor","Southeast Asia","British-resident sultanate",""),
("PHG","Pahang","Southeast Asia","Sultanate","Accepts a British Resident in 1888."),
("NSN","Negeri Sembilan","Southeast Asia","Confederation of Minangkabau states",""),
("KED","Kedah","Southeast Asia","Sultanate under Siamese suzerainty","Transferred to Britain in 1909."),
("KEL","Kelantan","Southeast Asia","Sultanate under Siamese suzerainty",""),
("TRG","Terengganu","Southeast Asia","Sultanate under Siamese suzerainty",""),
("PRL","Perlis","Southeast Asia","Sultanate under Siamese suzerainty",""),
("BRN","Brunei","Southeast Asia","Sultanate","Being eaten from both sides by Sarawak and the North Borneo Company."),
("SRW","Sarawak","Southeast Asia","Kingdom of the White Rajahs","Ruled by the Brooke family, an English dynasty of Malay rajahs."),
("NBO","North Borneo","Southeast Asia","Chartered company territory","Governed by the British North Borneo Company from 1881."),
("SLU","Sulu","Southeast Asia","Sultanate","Spanish suzerainty asserted 1878; still sovereign in practice."),
("ACE","Aceh","Southeast Asia","Sultanate at war with the Netherlands","The Aceh War has run since 1873 and will run until 1904."),
("DLI","Deli","Southeast Asia","Sultanate under Dutch protection","Sumatra's tobacco plantation belt."),
("SKI","Siak","Southeast Asia","Sultanate under Dutch protection","Sumatra."),
("KLU","Klungkung","Southeast Asia","Balinese kingdom","Nominal overlord of Bali; destroyed in the 1908 puputan."),
("BDG","Badung","Southeast Asia","Balinese kingdom",""),
("BLL","Buleleng","Southeast Asia","Balinese kingdom under Dutch control",""),
("LOM","Lombok","Southeast Asia","Balinese-ruled kingdom","A Balinese dynasty over a Sasak population; conquered by the Dutch in 1894."),
("TRN","Ternate","Southeast Asia","Sultanate under Dutch protection","Former spice power in the Moluccas."),
("TID","Tidore","Southeast Asia","Sultanate under Dutch protection",""),
("BNE","Bone","Southeast Asia","Bugis kingdom","South Sulawesi."),

# ---- East Asia ----
("QNG","Qing Empire","East Asia","Empire","HOI4's CHI is the Republic. The Qing is a different state -- Manchu dynasty, tributary system, Xinjiang made a province in 1884."),

# ---- North and Northeast Africa ----
("MHD","Mahdist State","Northeast Africa","Islamic state in Sudan","Took Khartoum in January 1885 and killed Gordon; rules Sudan until Omdurman in 1898."),
("DAR","Darfur","Northeast Africa","Sultanate under Mahdist control","Independent again 1898-1916."),
("WAD","Wadai","Central Africa","Sultanate",""),
("BGR","Baguirmi","Central Africa","Sultanate",""),
("BOR","Bornu","Central Africa","Kanem-Bornu empire","A thousand years old; overthrown by Rabih az-Zubayr in 1893."),

# ---- West Africa ----
("SOK","Sokoto Caliphate","West Africa","Caliphate","The largest state in nineteenth-century Africa; a federation of some thirty emirates."),
("ASH","Ashanti","West Africa","Empire","Weakened after 1874 but still independent; annexed 1902."),
("DAH","Dahomey","West Africa","Kingdom","Its standing corps of women soldiers is unique in Africa."),
("BNI","Benin","West Africa","Kingdom","Sacked by a British punitive expedition in 1897."),
("OYO","Oyo","West Africa","Yoruba empire in decline",""),
("IJE","Ijebu","West Africa","Yoruba kingdom","Controls the trade road to Lagos."),
("EGB","Egba","West Africa","Yoruba state at Abeokuta",""),
("WSU","Wassoulou","West Africa","Empire of Samori Toure","Fights France for sixteen years; Samori is captured in 1898."),
("TCL","Toucouleur Empire","West Africa","Empire","Ahmadu Tall's state on the upper Niger."),
("KND","Kenedougou","West Africa","Kingdom","Sikasso; its walls hold out against both Samori and France."),
("FTJ","Futa Jallon","West Africa","Imamate","Guinea highlands."),
("FTT","Futa Toro","West Africa","Imamate","Senegal river."),

# ---- Central and East Africa ----
("CFS","Congo Free State","Central Africa","Personal possession of Leopold II","Recognised at Berlin in 1885. Owned by a man, not a country."),
("BUG","Buganda","East Africa","Kingdom","Mwanga II; the Uganda martyrs are executed in 1886."),
("BUN","Bunyoro","East Africa","Kingdom","Kabalega's army resists Britain until 1899."),
("NKO","Nkore","East Africa","Kingdom","Ankole."),
("TRO","Toro","East Africa","Kingdom","Broke from Bunyoro in 1830."),
("RWA","Rwanda","East Africa","Kingdom","Still entirely unvisited by Europeans in 1886."),
("BDI","Burundi","East Africa","Kingdom",""),
("SHW","Shewa","Northeast Africa","Kingdom under Ethiopian suzerainty","Menelik II's power base; he becomes Emperor in 1889."),
("TGR","Tigray","Northeast Africa","Province under Ethiopian suzerainty","Yohannes IV's home province."),
("HRR","Harar","Northeast Africa","Emirate","Egypt withdrew in 1885; Menelik conquers it in 1887."),
("MJT","Majeerteen","East Africa","Somali sultanate","Northeast Somali coast."),
("HOB","Hobyo","East Africa","Somali sultanate",""),
("WIT","Witu","East Africa","Sultanate under German protection","A German protectorate 1885-1890, then traded to Britain."),

# ---- Southern Africa ----
("TVL","South African Republic","Southern Africa","Boer republic","The Transvaal. Gold is found on the Witwatersrand in 1886 and changes everything."),
("OFS","Orange Free State","Southern Africa","Boer republic","The model republic; constitutionally stable and prosperous."),
("ZUL","Zululand","Southern Africa","Partitioned kingdom","Broken up after 1879; a British protectorate from 1887."),
("NWR","New Republic","Southern Africa","Boer republic","Carved out of Zululand in 1884 by Boers paid in land; absorbed by the Transvaal in 1888."),
("SWZ","Swaziland","Southern Africa","Kingdom","Squeezed between the Transvaal and Britain."),
("BSU","Basutoland","Southern Africa","British protectorate","Moshoeshoe's kingdom; taken under direct Crown rule in 1884."),
("MTB","Matabeleland","Southern Africa","Kingdom","Lobengula's Ndebele state; loses everything to Rhodes's charter in 1890."),
("BRT","Barotseland","Southern Africa","Kingdom","Lewanika's Lozi state on the upper Zambezi."),
("BCH","Bechuanaland","Southern Africa","British protectorate","Declared in 1885 to keep the road north open."),
("MER","Merina","East Africa","Kingdom of Madagascar","A French protectorate was imposed in December 1885; the monarchy is abolished in 1897."),
("CAP","Cape Colony","Southern Africa","Self-governing British colony","Responsible government since 1872; Cecil Rhodes enters its parliament."),
("NTL","Natal","Southern Africa","British colony","Indian indentured labour arriving since 1860."),

# ---- Oceania ----
("HAW","Hawaii","Oceania","Kingdom","Kalakaua reigns; American planters impose the Bayonet Constitution in 1887."),
("SMA","Samoa","Oceania","Contested kingdom","Germany, Britain and the United States all back rival claimants."),
("TON","Tonga","Oceania","Kingdom","George Tupou I; never colonised."),
]

NOTES = """
Judgement calls behind this list
--------------------------------
Included although a HOI4 tag with a similar name exists, because the 1886 state
is a materially different polity:

  OTT  Ottoman Empire   TUR is the 1923 republic: different borders, different
                        subjects, no caliphate, no Arab provinces.
  RUS  Russian Empire   SOV is the Soviet Union. In 1886 the Tsar rules Finland
                        and Congress Poland, holds Bessarabia and Kars, and has
                        Khiva and Bukhara as protectorates.
  QNG  Qing Empire      CHI is the Republic. The Qing has a Manchu dynasty, a
                        tributary system and a court, none of which HOI4 models.
  PRS  Prussia          GER is the unified nation-state. In 1886 Prussia is one
                        of twenty-six members of a federal empire. Not PRU, which
                        vanilla already uses for Peru -- a collision the original
                        hand-written guard list missed entirely.

Excluded because the base game already covers them adequately for 1886:
Ethiopia, Liberia, Nepal, Bhutan, Siam, Persia, Afghanistan, Oman, Yemen, Korea,
Mongolia, Tibet, Morocco, Japan, and every independent republic in the Americas.
Brazil is an empire until 1889 rather than a republic, but the territory and tag
carry over, so it needs no new entry.

Excluded because they had already ceased to exist by 1886: the Ryukyu Kingdom
(annexed 1879), Kokand (1876), Yaqub Beg's Kashgaria (1877), Vientiane (1828),
and Tahiti (1880).

Burma is included even though Britain annexed it on 1 January 1886. If the
campaign opens earlier in the decade it is a playable kingdom; if it opens later
its annexation is the first event on the map.

Colonial administrations are included only where they behaved as distinct
political actors with their own parliaments, armies or charters -- the Cape,
Natal, North Borneo, Sarawak, the Congo Free State. Ordinary colonial provinces
are not countries and are left out.
"""


# Tags this list shares with the recovered geometry because BOTH name the same
# country -- the previous mod coined them independently and identically. These
# are agreement, not collision. PRU was the real collision: it meant Prussia
# here and Peru there, and Prussia moved to PRS.
SAME_COUNTRY = {
    "DAH": "Dahomey",
    "NKO": "Nkore",
    "OFS": "Orange Free State",
    "RUS": "Russian Empire",
}


def _owner_tags(path="tools/data/state_geometry_1886.tsv"):
    """Every tag that owns a state in the 1886 map."""
    out = set()
    try:
        with open(path, encoding="utf-8") as fh:
            for i, line in enumerate(fh):
                if i and len(line.split("\t")) > 4:
                    out.add(line.split("\t")[4].strip())
    except FileNotFoundError:
        pass
    return out


def check():
    seen = collections.Counter(r[0] for r in ROWS)
    dupes = [t for t, n in seen.items() if n > 1]
    clash = sorted(({r[0] for r in ROWS} & VANILLA) - set(SAME_COUNTRY))
    bad = [r[0] for r in ROWS if not (len(r[0]) == 3 and r[0].isalnum() and r[0].isupper())]
    print(f"entries: {len(ROWS)}")
    print(f"  duplicate tags:        {dupes or 'none'}")
    print(f"  clashes with vanilla:  {clash or 'none'}")
    print(f"  shared, same country:  {sorted(SAME_COUNTRY)}")
    print(f"  malformed tags:        {bad or 'none'}")
    by = collections.Counter(r[2] for r in ROWS)
    print("\n  by region:")
    for k, v in by.most_common():
        print(f"    {k:<18} {v}")
    return not (dupes or clash or bad)


# region -> (graphical culture, base hue 0-1, hue spread)
LOOK = {
    "German Empire":    ("western_european",  0.62, 0.10),
    "Balkans":          ("eastern_european",  0.78, 0.07),
    "Near East":        ("middle_eastern",    0.09, 0.04),
    "North Africa":     ("middle_eastern",    0.11, 0.03),
    "Arabia":           ("middle_eastern",    0.13, 0.06),
    "Central Asia":     ("middle_eastern",    0.05, 0.03),
    "India":            ("asian",             0.03, 0.08),
    "Southeast Asia":   ("asian",             0.42, 0.12),
    "East Asia":        ("asian",             0.16, 0.03),
    "Northeast Africa": ("african",           0.30, 0.06),
    "Central Africa":   ("african",           0.34, 0.05),
    "West Africa":     ("african",           0.24, 0.09),
    "East Africa":      ("african",           0.47, 0.08),
    "Southern Africa":  ("african",           0.55, 0.08),
    "Oceania":          ("commonwealth",      0.88, 0.05),
    "Australasia":      ("commonwealth",      0.94, 0.06),
    "Eastern Europe":   ("eastern_european",  0.70, 0.03),
}


def rgb_for(region, i, n):
    import colorsys
    if region not in LOOK:
        raise SystemExit(f"no colour/graphics rule for region {region!r}; add it to LOOK")
    gfx, base, spread = LOOK[region]
    h = (base + (spread * ((i / max(n - 1, 1)) - 0.5) * 2)) % 1.0
    s = 0.42 + 0.20 * ((i * 7) % 5) / 4.0
    v = 0.55 + 0.28 * ((i * 3) % 4) / 3.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255), gfx


def fname(name):
    keep = "".join(c if (c.isalnum() or c in " -") else "" for c in name)
    return keep.strip().replace(" ", "_") + ".txt"


def write(mod="MOD", docs="MOD/documentation"):
    os.makedirs(f"{mod}/common/country_tags", exist_ok=True)
    os.makedirs(f"{mod}/common/countries", exist_ok=True)
    os.makedirs(docs, exist_ok=True)

    per_region = collections.defaultdict(list)
    for r in ROWS:
        per_region[r[2]].append(r)

    tags, colors = [], []
    used = set()
    for region, rows in per_region.items():
        for i, (tag, name, _reg, status, note) in enumerate(rows):
            red, green, blue, gfx = rgb_for(region, i, len(rows))
            # every country needs a distinct map colour; nudge on collision
            while (red, green, blue) in used:
                red = (red + 7) % 256
                green = (green + 3) % 256
            used.add((red, green, blue))
            f = fname(name)
            tags.append((tag, f, name))
            colors.append((tag, red, green, blue))
            with open(f"{mod}/common/countries/{f}", "w", encoding="utf-8") as fh:
                fh.write(f"# {name} -- {status}\n")
                fh.write(f"graphical_culture = {gfx}_gfx\n")
                fh.write(f"graphical_culture_2d = {gfx}_2d\n")

    tags.sort(key=lambda x: x[0])
    # NOT 00_countries.txt. Hearts of Iron IV overrides common/country_tags by
    # filename, and 00_countries.txt is vanilla's own -- shipping that name
    # deletes all ~190 base-game tags, leaving every state owned by FRA, ENG,
    # USA and 70 others with no country behind it. A distinct filename is
    # additive: vanilla's tags load, and these are added on top.
    tagfile = f"{mod}/common/country_tags/01_dsa_1886_countries.txt"
    with open(tagfile, "w", encoding="utf-8") as fh:
        fh.write("# Countries present in 1886 that Hearts of Iron IV does not model.\n")
        fh.write("# Generated by tools/countries_1886.py -- edit that file, not this one.\n")
        fh.write("# Filename is deliberately not 00_countries.txt; see that script.\n\n")
        for tag, f, name in tags:
            fh.write(f'{tag} = "countries/{f}"'.ljust(52) + f"# {name}\n")

    # colors.txt IS vanilla's filename and there is no alternative the game
    # reads, so this file genuinely replaces the base game's. That means it has
    # to carry a colour for every tag the mod uses, including the vanilla ones
    # it would otherwise blank. Tags without a hand-picked colour get a stable
    # one derived from the tag itself.
    import colorsys as _cs
    have = {c[0] for c in colors}
    for tag in sorted(_owner_tags()):
        if tag in have:
            continue
        h = (sum(ord(c) * (i + 3) for i, c in enumerate(tag)) % 360) / 360.0
        s = 0.45 + ((ord(tag[0]) * 7) % 5) / 12.0
        v = 0.55 + ((ord(tag[-1]) * 3) % 4) / 10.0
        rr, gg, bb = _cs.hsv_to_rgb(h, s, v)
        rgbv = (int(rr * 255), int(gg * 255), int(bb * 255))
        while rgbv in used:
            rgbv = ((rgbv[0] + 7) % 256, (rgbv[1] + 3) % 256, rgbv[2])
        used.add(rgbv)
        colors.append((tag, *rgbv))

    colors.sort()
    with open(f"{mod}/common/countries/colors.txt", "w", encoding="utf-8") as fh:
        fh.write("# Generated by tools/countries_1886.py\n")
        fh.write("# This filename is vanilla's, so this file REPLACES the base game's\n")
        fh.write("# colours. It therefore covers every tag the mod uses, vanilla\n")
        fh.write("# ones included -- otherwise France and Britain would have none.\n\n")
        for tag, r_, g_, b_ in colors:
            fh.write(f"{tag} = {{\n\tcolor = rgb {{ {r_} {g_} {b_} }}\n")
            fh.write(f"\tcolor_ui = rgb {{ {r_} {g_} {b_} }}\n}}\n")

    with open(f"{mod}/localisation/countries_1886_l_english.yml", "w", encoding="utf-8-sig") as fh:
        fh.write("l_english:\n")
        for tag, f, name in tags:
            fh.write(f' {tag}:0 "{name}"\n')
            fh.write(f' {tag}_DEF:0 "{name}"\n')

    with open(f"{docs}/1886-COUNTRIES.md", "w", encoding="utf-8") as fh:
        fh.write("# The 1886 world, minus what Hearts of Iron IV already has\n\n")
        fh.write(f"**{len(ROWS)} polities** that existed in 1886 and have no vanilla HOI4 equivalent.\n\n")
        fh.write("Generated by `tools/countries_1886.py`. Edit that file and re-run;\n")
        fh.write("do not edit the generated tag, colour or localisation files by hand.\n\n")
        order = sorted(per_region, key=lambda r: -len(per_region[r]))
        fh.write("| Region | Count |\n|---|---|\n")
        for region in order:
            fh.write(f"| {region} | {len(per_region[region])} |\n")
        fh.write("\n")
        for region in order:
            fh.write(f"\n## {region}\n\n")
            fh.write("| Tag | Country | Status in 1886 | Notes |\n|---|---|---|---|\n")
            for tag, name, _r, status, note in sorted(per_region[region], key=lambda x: x[1]):
                fh.write(f"| `{tag}` | {name} | {status} | {note} |\n")
        fh.write("\n## Notes\n\n```")
        fh.write(NOTES)
        fh.write("```\n")

    print(f"wrote {len(tags)} tags, {len(tags)} country files, colours, localisation")
    print(f"  {tagfile}")
    print(f"  {mod}/common/countries/*.txt")
    print(f"  {mod}/common/countries/colors.txt")
    print(f"  {mod}/localisation/countries_1886_l_english.yml")
    print(f"  {docs}/1886-COUNTRIES.md")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    ok = check()
    if not ok:
        sys.exit(1)
    if a.write:
        print()
        write()
