version="0.4"
tags={
	"Alternative History"
	"Historical"
	"Map"
}
name="Divided States of America"
supported_version="1.19.*"
# Vanilla's versions of these directories must not load alongside the mod's.
# The game merges each by filename, so vanilla's 50-Wurttemberg.txt would
# survive next to this mod's own state 50 and the id would be defined twice --
# exactly what left the previous version with 65 duplicate state ids.
# Countries are the same problem in a different form: vanilla's files set up
# 1936 cabinets and armies for nations that in 1886 looked nothing alike.
# Bookmarks matter because vanilla's start in 1936 and 1939, and this world is
# 1886.
replace_path="history/states"
replace_path="history/countries"
replace_path="history/units"
replace_path="common/bookmarks"
