# ---------------------------------------------------------------------------
# COPY THIS FILE into your Hearts of Iron IV mod folder, next to the mod folder
# itself, and change ONLY the last line.
#
#   Documents/Paradox Interactive/Hearts of Iron IV/mod/
#       dsa/        <- the contents of MOD/
#       dsa.mod     <- this file
#
# The replace_path lines are not optional and not decoration. Hearts of Iron IV
# merges these directories with vanilla's BY FILENAME. Without them, vanilla's
# ~800 states load alongside this mod's 857 and every shared id is defined
# twice -- which is exactly the fault that made the previous version of this
# mod unplayable.
#
# They only take effect in THIS file, the one the launcher reads. Putting them
# in descriptor.mod inside the folder does nothing. Two test cycles were lost
# to that before.
# ---------------------------------------------------------------------------
version="0.5"
tags={
	"Alternative History"
	"Historical"
	"Map"
}
name="Divided States of America"
supported_version="1.19.*"
replace_path="history/states"
replace_path="history/countries"
replace_path="history/units"
replace_path="common/bookmarks"
# map/supplyareas is part of the map definition. The mod creates 57 states by
# splitting vanilla ones and drops 12 that ended up empty, so vanilla's supply
# areas both miss states and name states that no longer exist. Either is a
# broken reference in the map definition, and the game refuses to load the map.
replace_path="map/supplyareas"
# The rest of map/ ships WITHOUT replace_path, and must keep doing so. The map
# this mod is built on is vanilla's with 678 extra land provinces carved into
# Africa, South America, Persia and the Balkans, so definition.csv and
# provinces.bmp have to ship or the states name provinces the game has never
# heard of. But only the 82 strategic regions those provinces fall in are
# shipped; declaring replace_path="map" would delete the ~128 vanilla regions
# that cover the rest of the world and strand every province in them.

# Change the line below to where you put the mod folder.
# Forward slashes, even on Windows. No trailing slash.
path="C:/Users/CHANGEME/Documents/Paradox Interactive/Hearts of Iron IV/mod/dsa"
