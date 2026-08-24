version="0.2"
tags={
	"Alternative History"
	"Historical"
	"Map"
}
name="Divided States of America"
supported_version="1.19.*"
# The mod defines the whole world's states. Vanilla's history/states must not
# load alongside them: the game merges that directory by filename, so vanilla's
# 50-Wurttemberg.txt would survive next to this mod's own state 50 and the id
# would be defined twice. That is exactly what left the previous version with
# 65 duplicate state ids.
replace_path="history/states"
