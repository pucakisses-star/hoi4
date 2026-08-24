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
version="0.4"
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

# Change the line below to where you put the mod folder.
# Forward slashes, even on Windows. No trailing slash.
path="C:/Users/CHANGEME/Documents/Paradox Interactive/Hearts of Iron IV/mod/dsa"
