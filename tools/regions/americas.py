"""
The Americas, 1886.

Most of this is whole-state inheritance: every Latin American republic already
existed by 1886 with borders close enough to 1936 that vanilla's states carry
over. Four things genuinely differ, and one is a design decision rather than a
historical fact.

The design decision: **North America stays divided.** The recovered geometry
carries a fully worked-out alternate United States from the previous mod --
a Confederacy of eleven states, California, Texas, Deseret in Utah, an Aztec
state across New Mexico and Arizona, and Cascadia across Washington and Oregon.
That is the premise the mod is named for, so it is preserved rather than
overwritten with a single historical USA. It is the author's to change; nothing
here asserts it is history.

What is history, and differs from 1936:

  - Cuba and Puerto Rico are Spanish. The United States takes them in 1898.
  - Panama is Colombian. It does not separate until 1903, so the isthmus and
    the canal zone both go to Colombia.
  - Hawaii is an independent kingdom under Kalakaua, annexed only in 1898.
  - Samoa is a contested independent kingdom, not a New Zealand possession.
  - Newfoundland and Labrador are a separate British colony, not Canadian.
    Canada is a self-governing Dominion, which it has been since 1867.
  - Brazil is an empire under Pedro II until 1889, but the tag is unchanged.

Peru is PRU here, which is what vanilla calls it. Prussia is PRS: assigning
Prussia to PRU earlier collided with five Peruvian states.
"""

_WHOLE = {
    "USA": ["Alaska", "North Dakota", "Montana", "Minnesota", "Wisconsin",
            "South Dakota", "Idaho", "Michigan", "Massachusetts", "New York",
            "Wyoming", "Iowa", "Nebraska", "Pennsylvania", "Ohio", "New Jersey",
            "Nevada", "Illinois", "Indiana", "Maryland", "Colorado", "Kansas",
            "Missouri", "Kentucky", "Midway Island", "Johnston Atoll",
            "Line Islands", "Phoenix Island"],
    # --- the previous mod's divided America, preserved deliberately ---
    "COF": ["Virginia", "Tennessee", "North Carolina", "Oklahoma", "Arkansas",
            "South Carolina", "Alabama", "Mississippi", "Georgia", "Louisiana",
            "Florida"],
    "CAL": ["California"],
    "TEX": ["Texas"],
    "CDA": ["Washington", "Oregon"],
    "AZT": ["New Mexico", "Arizona"],
    "DES": ["Utah"],

    "CAN": ["Northern Canada", "Northwestern Canada", "Northeastern Canada",
            "Quebec", "Alberta", "Haida Gwaii", "Saskatchewan", "British Columbia",
            "Manitoba", "Vancouver Island", "Northern Ontario", "Saint Lawrence",
            "New Brunswick", "Nova Scotia", "Southern Ontario"],
    "ENG": ["Labrador", "Newfoundland", "Bermuda", "Northern Bahamas",
            "Southern Bahamas", "Jamaica", "British Honduras", "Leeward Islands",
            "Windward Islands", "Trinidad", "British Guyana", "Pitcairn Island",
            "Falkland Islands", "South Georgia"],
    "MEX": ["Sonora", "Chihuahua", "Baja California", "Coahuila", "Durango",
            "Tamaulipas", "Jalisco", "Mexico City", "Veracruz", "Yucatan",
            "Guerrero", "Oaxaca", "Chiapas"],
    "BRA": ["Amazonas", "Maranhao", "Rio Grande do Norte", "Mato Grosso", "Bahia",
            "Goias", "Para", "Piaui", "Rio de Janeiro", "Sao Paulo",
            "Santa Catarina", "Rio Grande do Sul"],
    "ARG": ["Buenos Aires", "Tucuman", "Mesopotamia", "Mendoza", "Pampas",
            "Patagonia"],
    "CHL": ["Atacama", "Santiago", "Magallanes"],
    "URG": ["Montevideo"],
    "PRU": ["Pastaza", "Loreto", "San Martin", "Ucayali", "Arequipa"],  # Peru
    "BOL": ["Santa Cruz", "La Paz"],
    "VEN": ["Zulia", "Miranda", "Bolivar"],
    "PAR": ["Chaco Boreal", "Neembucu"],
    "ECU": ["Ecuador", "Galapagos Islands"],
    "DOM": ["Cibao"],
    "HAI": ["Port au Prince"],
    "NIC": ["Nicaragua"], "GUA": ["Guatemala"], "HON": ["Honduras"],
    "COS": ["Costa Rica"], "ELS": ["El Salvador"],
    "DEN": ["Greenland"],
    "HOL": ["Curacao", "Suriname"],
    "POR": ["Azores"],
    "FRA": ["St Pierre and Miquelon", "French Caribbean", "French Guiana",
            "Tahiti"],   # Tahiti annexed 1880

    # --- the genuine 1886 corrections ---
    "SPR": ["Cuba", "Puerto Rico"],           # Spanish until 1898
    "COL": ["La Libertad", "Cundinamarca", "Meta",
            "Panama", "Panama Canal"],        # Panama is Colombian until 1903
    "HAW": ["Hawaii"],                        # independent kingdom under Kalakaua
    "SMA": ["Samoa"],                         # contested independent kingdom
}

SPLIT = {}
for _tag, _states in _WHOLE.items():
    for _n in _states:
        SPLIT[_n] = {_tag: None}

NAMES = {
    "USA": "United States", "COF": "Confederate States", "CAL": "California",
    "TEX": "Texas", "CDA": "Cascadia", "AZT": "Aztec", "DES": "Deseret",
    "CAN": "Canada", "ENG": "United Kingdom", "MEX": "Mexico", "BRA": "Brazil",
    "ARG": "Argentina", "CHL": "Chile", "URG": "Uruguay", "PRU": "Peru",
    "BOL": "Bolivia", "VEN": "Venezuela", "COL": "Colombia", "PAR": "Paraguay",
    "ECU": "Ecuador", "DOM": "Dominican Republic", "HAI": "Haiti",
    "NIC": "Nicaragua", "GUA": "Guatemala", "HON": "Honduras",
    "COS": "Costa Rica", "ELS": "El Salvador", "DEN": "Denmark",
    "HOL": "Netherlands", "POR": "Portugal", "FRA": "France", "SPR": "Spain",
    "HAW": "Hawaii", "SMA": "Samoa",
}
