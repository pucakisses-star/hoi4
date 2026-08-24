version="0.3"
tags={
	"Alternative History"
	"Historical"
	"Map"
}
name="Divided States of America"
supported_version="1.19.*"
# The mod defines the whole world's states and every country that holds one.
# Vanilla's directories must not load alongside them. The game merges both by
# filename, so vanilla's 50-Wurttemberg.txt would survive next to this mod's
# own state 50 and the id would be defined twice -- exactly what left the
# previous version with 65 duplicate state ids. The country directory is the
# same problem in a different form: vanilla's files set up 1936 cabinets,
# technology and armies for countries that in 1886 looked nothing alike.
replace_path="history/states"
replace_path="history/countries"
