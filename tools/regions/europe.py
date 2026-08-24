"""
Europe outside the German Empire and the Habsburg lands, 1886.

Almost all of this is whole-state inheritance -- the borders of France, Iberia,
Italy, the Low Countries and Scandinavia in 1886 are close enough to 1936 that
vanilla's states carry over unchanged. What does change is who owns the east and
the north-west:

  - Poland, Lithuania, Latvia, Estonia, Belarus and Ukraine are not countries.
    They are governorates of the Russian Empire and go to RUS.
  - Ireland is not a country either. The United Kingdom of Great Britain and
    Ireland is one state until 1922, so IRE goes to ENG.
  - Finland keeps its own tag. It is Russian, but as a Grand Duchy with its own
    diet, currency, postal service and army -- the same autonomous-subject case
    as Croatia-Slavonia under Hungary.
  - Norway keeps its own tag: in personal union with Sweden under Oscar II, but
    a separate kingdom with its own constitution.

Lebanon and Tunisia were briefly in this table and are not in Europe. They were
swept in by a latitude/longitude box computed with the Central European
projection, which is badly wrong at their longitude, and it put Mount Lebanon
under France thirty-four years before the mandate. Regions are not defined by a
projection box any more; a state is in a region because it is listed here.

Anatolia and Mosul are deliberately NOT here. They are Ottoman, but Russia took
Kars, Ardahan and Batumi in 1878 and carving those out needs a Caucasus
projection fit; the Central European one is unreliable that far east. They are
left for a Near East region rather than assigned to a border that is known to be
wrong.
"""

SPLIT = {
    # --- RUS: the Tsar's European empire: Congress Poland, the Baltic governorates,
    # Belarus, Ukraine, Bessarabia and the Caucasus are all provinces of it in 1886 ---
    "Akhtubinsk":                       {"RUS": None},
    "Arkhangelsk":                      {"RUS": None},
    "Armenia":                          {"RUS": None},
    "Astrakhan":                        {"RUS": None},
    "Azerbaijan":                       {"RUS": None},
    "Belgorod":                         {"RUS": None},
    "Bialystok":                        {"RUS": None},
    "Bobruysk":                         {"RUS": None},
    "Bryansk":                          {"RUS": None},
    "Cheboksary":                       {"RUS": None},
    "Chelyabinsk":                      {"RUS": None},
    "Cherkasy":                         {"RUS": None},
    "Chernihiv":                        {"RUS": None},
    "Crimea":                           {"RUS": None},
    "Elista":                           {"RUS": None},
    "Gomel":                            {"RUS": None},
    "Guryev":                           {"RUS": None},
    "Harju":                            {"RUS": None},
    "Hughesovka":                       {"RUS": None},
    "Imereti":                          {"RUS": None},
    "Ivanovo":                          {"RUS": None},
    "Izhevsk":                          {"RUS": None},
    "Kalisz":                           {"RUS": None},
    "Kaluga":                           {"RUS": None},
    "Kaunas":                           {"RUS": None},
    "Kazan":                            {"RUS": None},
    "Kharkov":                          {"RUS": None},
    "Kherson":                          {"RUS": None},
    "Khiva":                            {"RUS": None},
    "Khmelnytskyi":                     {"RUS": None},
    "Kielce":                           {"RUS": None},
    "Kiev":                             {"RUS": None},
    "Kursk":                            {"RUS": None},
    "Kurzeme":                          {"RUS": None},
    "Kustanay":                         {"RUS": None},
    "Kyzyl Orda":                       {"RUS": None},
    "Lipetsk":                          {"RUS": None},
    "Lublin":                           {"RUS": None},
    "Luga":                             {"RUS": None},
    "Luganskiy Zavod":                  {"RUS": None},
    "Magnitogorsk":                     {"RUS": None},
    "Mazowsze":                         {"RUS": None},
    "Memel":                            {"RUS": None},
    "Mikhaylovka":                      {"RUS": None},
    "Millerovo":                        {"RUS": None},
    "Minsk":                            {"RUS": None},
    "Moscow Area":                      {"RUS": None},
    "Mozyr":                            {"RUS": None},
    "Murmansk":                         {"RUS": None},
    "Mykolaiv":                         {"RUS": None},
    "Nevel":                            {"RUS": None},
    "Nizhny Novgorod":                  {"RUS": None},
    "Northern Urals":                   {"RUS": None},
    "Novgorod":                         {"RUS": None},
    "Nowogrodek":                       {"RUS": None},
    "Odessa":                           {"RUS": None},
    "Olonets":                          {"RUS": None},
    "Onega":                            {"RUS": None},
    "Orel":                             {"RUS": None},
    "Orenburg":                         {"RUS": None},
    "Pechora":                          {"RUS": None},
    "Penza":                            {"RUS": None},
    "Perm":                             {"RUS": None},
    "Plock":                            {"RUS": None},
    "Polesie":                          {"RUS": None},
    "Poltava":                          {"RUS": None},
    "Pskov":                            {"RUS": None},
    "Roslavl":                          {"RUS": None},
    "Rostov":                           {"RUS": None},
    "Ryazan":                           {"RUS": None},
    "Rzhev":                            {"RUS": None},
    "Samara#251":                       {"RUS": None},
    "Samara#401":                       {"RUS": None},
    "Sankt Petersburg":                 {"RUS": None},
    "Saratov":                          {"RUS": None},
    "Siauliai":                         {"RUS": None},
    "Smolensk":                         {"RUS": None},
    "South Dagestan":                   {"RUS": None},
    "Stravropol":                       {"RUS": None},
    "Sumy":                             {"RUS": None},
    "Tambov":                           {"RUS": None},
    "Tartu":                            {"RUS": None},
    "Tashkent":                         {"RUS": None},
    "Tikhvin":                          {"RUS": None},
    "Tobolsk":                          {"RUS": None},
    "Tsaritsyn":                        {"RUS": None},
    "Tula":                             {"RUS": None},
    "Tver":                             {"RUS": None},
    "Ufa":                              {"RUS": None},
    "Ulyanovsky":                       {"RUS": None},
    "Uralsk":                           {"RUS": None},
    "Urgench":                          {"RUS": None},
    "Ust Urt":                          {"RUS": None},
    "Ust-Sysolsk":                      {"RUS": None},
    "Vidzeme":                          {"RUS": None},
    "Vinnytsia":                        {"RUS": None},
    "Vitebsk":                          {"RUS": None},
    "Volgodonsk":                       {"RUS": None},
    "Volkhov":                          {"RUS": None},
    "Vologda":                          {"RUS": None},
    "Voronezh":                         {"RUS": None},
    "Vyatka":                           {"RUS": None},
    "Western Circassia":                {"RUS": None},
    "Wolyn":                            {"RUS": None},
    "Yaroslavl":                        {"RUS": None},
    "Yekaterinburg":                    {"RUS": None},
    "Yekaterinodar":                    {"RUS": None},
    "Yekaterinoslav":                   {"RUS": None},
    "Zaporozhe":                        {"RUS": None},
    "Zhytomyr":                         {"RUS": None},
    "Zlatoust":                         {"RUS": None},

    # --- FRA ---
    "Aleppo":                           {"FRA": None},
    "Algiers":                          {"FRA": None},
    "Alpes":                            {"FRA": None},
    "Aquitaine":                        {"FRA": None},
    "Auvergne":                         {"FRA": None},
    "Basse-Normandie":                  {"FRA": None},
    "Bretagne":                         {"FRA": None},
    "Burgundy":                         {"FRA": None},
    "Centre":                           {"FRA": None},
    "Champagne":                        {"FRA": None},
    "Charente":                         {"FRA": None},
    "Constantine":                      {"FRA": None},
    "Corsica":                          {"FRA": None},
    "Deir-az-Zur":                      {"FRA": None},
    "Franche-Comté":                    {"FRA": None},
    "Gascogne":                         {"FRA": None},
    "Ile de France":                    {"FRA": None},
    "Languedoc-Roussillion":            {"FRA": None},
    "Limousin":                         {"FRA": None},
    "Maine":                            {"FRA": None},
    "Picardie":                         {"FRA": None},
    "Provence":                         {"FRA": None},
    "Pyrenees":                         {"FRA": None},
    "Rhone":                            {"FRA": None},
    "Savoy":                            {"FRA": None},
    "Vatican City":                     {"FRA": None},

    # --- SPR: the Restoration monarchy; Alfonso XIII is born in May 1886 ---
    "Andalusia":                        {"SPR": None},
    "Aragon":                           {"SPR": None},
    "Balearic Islands":                 {"SPR": None},
    "Castille":                         {"SPR": None},
    "Catalonia":                        {"SPR": None},
    "Er Rif":                           {"SPR": None},
    "Extremadura":                      {"SPR": None},
    "Galicia":                          {"SPR": None},
    "Granada":                          {"SPR": None},
    "La Mancha":                        {"SPR": None},
    "Leon":                             {"SPR": None},
    "Madrid Area":                      {"SPR": None},
    "Murcia":                           {"SPR": None},
    "Navarre":                          {"SPR": None},
    "Sarata":                           {"SPR": None},
    "Valencia":                         {"SPR": None},

    # --- ENG: the United Kingdom of Great Britain AND Ireland -- no partition until 1922 ---
    "Aberdeenshire":                    {"ENG": None},
    "Connaught":                        {"ENG": None},
    "Cornwall":                         {"ENG": None},
    "Cyprus":                           {"ENG": None},
    "East Anglia":                      {"ENG": None},
    "East Midlands":                    {"ENG": None},
    "Gibraltar":                        {"ENG": None},
    "Gloucestershire":                  {"ENG": None},
    "Greater London Area":              {"ENG": None},
    "Lanark":                           {"ENG": None},
    "Lancashire":                       {"ENG": None},
    "Leinster":                         {"ENG": None},
    "Lothian":                          {"ENG": None},
    "Malta":                            {"ENG": None},
    "Munster":                          {"ENG": None},
    "Northern England":                 {"ENG": None},
    "Northern Ireland":                 {"ENG": None},
    "Scottish Highlands":               {"ENG": None},
    "Sussex":                           {"ENG": None},
    "Wales":                            {"ENG": None},
    "West Midlands":                    {"ENG": None},
    "Yorkshire":                        {"ENG": None},

    # --- ITA: the Kingdom of Italy, unified since 1870; the Pope holds no territory ---
    "Calabria":                         {"ITA": None},
    "Campania":                         {"ITA": None},
    "Lazio":                            {"ITA": None},
    "Lombardy":                         {"ITA": None},
    "Piedmont":                         {"ITA": None},
    "Romagna":                          {"ITA": None},
    "Sardinia":                         {"ITA": None},
    "Sicily":                           {"ITA": None},
    "South Tyrol":                      {"ITA": None},
    "Spoleto":                          {"ITA": None},
    "Tuscany":                          {"ITA": None},
    "Veneto":                           {"ITA": None},

    # --- SWE ---
    "Gotland":                          {"SWE": None},
    "Lappland":                         {"SWE": None},
    "Norrland":                         {"SWE": None},
    "Scania":                           {"SWE": None},
    "Smaland":                          {"SWE": None},
    "Svealand":                         {"SWE": None},
    "Vastergotland":                    {"SWE": None},

    # --- FIN: the Grand Duchy of Finland: Russian, but with its own diet, currency,
    # postal service and army, so it keeps a tag the way Croatia-Slavonia does ---
    "Aland":                            {"FIN": None},
    "Karjala":                          {"FIN": None},
    "Lappi":                            {"FIN": None},
    "Petsamo":                          {"FIN": None},
    "Pohjanmaa":                        {"FIN": None},
    "Salla":                            {"FIN": None},
    "Savo":                             {"FIN": None},
    "Uusimaa":                          {"FIN": None},

    # --- NOR: in personal union with Sweden under Oscar II, but a separate kingdom ---
    "Nord-Norge":                       {"NOR": None},
    "Ostlandet":                        {"NOR": None},
    "Trondelag":                        {"NOR": None},
    "Vestlandet":                       {"NOR": None},

    # --- POR ---
    "Alentejo-Algarve":                 {"POR": None},
    "Guarda":                           {"POR": None},
    "Laristan":                         {"POR": None},
    "Lisbon":                           {"POR": None},
    "Porto":                            {"POR": None},

    # --- DEN: including Iceland and the Faroes ---
    "Faroe Islands":                    {"DEN": None},
    "Iceland":                          {"DEN": None},
    "Jutland":                          {"DEN": None},
    "Sjaelland":                        {"DEN": None},

    # --- HOL ---
    "Brabant":                          {"HOL": None},
    "Friesland":                        {"HOL": None},
    "Noord-Holland":                    {"HOL": None},

    # --- BEL ---
    "Flanders":                         {"BEL": None},
    "Namur":                            {"BEL": None},

    # --- SWI ---
    "Eastern Switzerland":              {"SWI": None},
    "Romandy":                          {"SWI": None},

    # --- LUX ---
    "Luxemburg":                        {"LUX": None},
}

NAMES = {
    "RUS": "Russian Empire", "FRA": "France", "SPR": "Spain", "ENG": "United Kingdom",
    "ITA": "Italy", "SWE": "Sweden", "FIN": "Finland", "NOR": "Norway",
    "POR": "Portugal", "DEN": "Denmark", "HOL": "Netherlands", "BEL": "Belgium",
    "SWI": "Switzerland", "LUX": "Luxembourg",
}
