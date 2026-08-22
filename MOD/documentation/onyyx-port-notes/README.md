# Onyyx port notes — preserved bug list

`Notes.txt` in this directory is a byte-identical copy of `Onyyx/Notes.txt`
(SHA-256 `f67a96c3ec65995083687ac692657fc610587c7a4801ebadc41b323728de5506`).
It was rescued into `MOD/` because it is the only hand-written bug
documentation anywhere in this repository, and the secondary mod folders it
lived in are slated for removal.

## Read this before acting on it

The notes were written by someone porting the Divided States of America
content into **Kaiserreich**, not into this mod. That matters in two ways:

1. Many entries are phrased as *"I fixed it"* — meaning fixed in **Onyyx's
   copy**, which is a different tree. Those fixes were never applied here.
2. A few entries are Kaiserreich-specific and do not apply to `MOD/` at all
   (notably #31 retagging California to `CLF` because Kaiserreich already
   uses `CAL`, #32 on Kaiserreich's `colors.txt`, and #33 on a Kaiserreich
   Madagascar/Madras tag conflict).

So treat the file as a *report of defects observed in the shared source
material*, not as a changelog for this mod.

## Verification against MOD/

Each item below was checked mechanically against `MOD/` at the time this
directory was created. Items not listed were **not** checked.

| # | Claim | Status in `MOD/` | Evidence |
|---|---|---|---|
| 4 / 10 | California party popularities sum to 101 | **still open** | `history/countries/CAL - California.txt` — 56 + 13 + 31 + 1 = 101 |
| 13 | `00_countries.txt` points at misspelled country filenames | **still open** | `COF = "countries/ConfederateStates.txt"` and `USA = "countries/UnitedStates.txt"` both resolve to nothing; the real file is `Confederate States.txt` (with a space) |
| 16 | `PRC` tag used twice | **partially open** | tag itself is defined once (`PRC = "countries/ComChina.txt"`), but two history files claim it: `PRC - ComChina.txt` and `PRC - People's Republic of California.txt` |
| 17 | Confederate capital is invalid state `10343` | **still open** | `history/countries/COF - Confederate States.txt:1` — `capital = 10343` |
| 18 | William C. Kibbe and MacArthur share `id = 57` | **not reproduced** | only one `id = 57` remains, in `USA - USA.txt:342` |
| 22 | Deseret adds Brigham Young twice | **still open** | 2 occurrences in `DES - Deseret.txt` |
| 23 | Two focus trees both claim Confederates | **not reproduced** | only `common/national_focus/csa.txt` sets `country = COF` |
| 26 | `00_ideologies.txt` has no `neutrality` entry | **still open** | zero `neutrality =` matches in `common/ideologies/00_ideologies.txt` |
| 28 | Event `cof.6` grants non-existent `unpopular_president` | **not reproduced** | no `unpopular_president` reference found |
| 34 | Alaska capital set to 362 (Virginia) instead of 463 | **still open, compounded** | *both* `ALK - Alaksa.txt` (`capital = 463`) and `ALK - Alaska.txt` (`capital = 362`) exist and both load — see below |

## Related defects found independently

These are not in `Notes.txt` but were found while verifying it, and share a
root cause: the Divided States content was appended onto a Victorian-era base
mod without reconciling the two.

- **Duplicate tag definitions.** `common/country_tags/00_countries.txt`
  defines `USA` at both line 66 (`countries/USA.txt`) and line 235
  (`countries/UnitedStates.txt`), and `PER` at line 55 (`countries/Persia.txt`)
  and line 236 (`countries/People'sRepublicofCalifornia.txt`). The last
  definition wins, so Persia and the base USA are both clobbered by entries
  pointing at files that do not exist. `PER`'s localisation is still entirely
  Persia, so People's Republic of California would display as "Qajar Dynasty".

- **70 of 232 tag definitions reference missing country files.**

- **13 tags have two history files each**, so the game loads both:
  `ALK`, `BAN`, `BAS`, `BOS`, `DAK`, `GDC`, `GUA`, `MOL`, `NIR`, `PNG`,
  `PRC`, `PUE`, `ZUL`. Several are typo pairs (`ALK - Alaksa.txt` alongside
  `ALK - Alaska.txt`, `GUA - Guatemla.txt` alongside `GUA - Guatemala.txt`).

- **Localisation for the new nations is incomplete.** `TEX`, `DAK`, `ALK` and
  `HAW` have full name sets; `COF`, `CDA`, `DES`, `AZT`, `NEW`, `JFR`, `VER`
  and `VEG` have none; `CAL` has 2 of roughly 30.

By contrast the scripting itself is clean: all 1,984 event definitions and all
5,738 focus definitions were checked for ID collisions and there are none. The
damage is confined to the tag, history-file and localisation wiring where the
two mods were joined.
