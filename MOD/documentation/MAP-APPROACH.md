# Map approach

The previous attempt died in this layer. Its `history/states/` held two redraws
of the same world stacked on top of each other: 1,735 provinces claimed by more
than one state, 65 duplicate state ids, 329 land provinces belonging to no state
at all. None of that appears in `error.log`, because the map is read by native
code rather than the script parser. It is worth being explicit about how this
attempt avoids repeating it.

## Ship no map at all

The mod does **not** include `map/`. No `provinces.bmp`, no `definition.csv`, no
`strategicregions`, no `supplyareas`. Vanilla's province map is inherited whole.

The previous mod shipped a full `map/` directory of 103 MB. Checked against its
own `definition.csv`, that map turned out to be unmodified vanilla: 13,882
provinces numbered contiguously from 0, the standard terrain set, the standard
seven continents, and — verified pixel by pixel against `provinces.bmp` — not a
single colour in the bitmap missing from the definition table. It was a copy,
not a change. All it bought was 103 MB, a `provinces.psd` the game never reads,
and the risk of drifting out of sync the next time Paradox patches the map.

Redrawing the province map is the one genuinely expensive thing in Hearts of
Iron IV modding and the most crash-prone. 10,623 land provinces at a median of
six neighbours each is enough resolution to draw 1886 borders without touching
a pixel. Provinces are the substrate; states are the politics. Only the politics
changed between 1886 and 1936.

## One state geometry, generated from one table

`tools/data/state_geometry.tsv` is the single source of truth for state shape:
one row per state, holding its id, localisation key, display name, category and
province list. State files are generated from it. Nothing else defines a state's
extent, so two layouts cannot drift apart, because there is only one.

The table was recovered rather than invented. Vanilla's own geometry was still
present in the old mod, in the id range 1–800, under renamed files — `1-France.txt`
contains `name="STATE_1" # Corsica` and vanilla's exact three provinces. Isolated
from the overlay above id 800 it was 800 states with no duplicate ids, but 119
provinces double-claimed and 949 land provinces short of complete, because the
overlay had taken provinces out of vanilla states without deleting the originals.

`tools/build_state_geometry.py` repairs that into a partition. Both defects take
the same rule: a province belongs to the state owning most of the provinces it
physically touches. Adjacency comes from `provinces.bmp` itself — 41,036
neighbour pairs read straight out of the bitmap by
`tools/province_adjacency.py`, with no image library. Orphans resolve in repeated
passes, since an orphan's neighbours may themselves be orphans; each pass only
decides provinces that touch settled territory, so the frontier grows inward.
Twenty island provinces whose only neighbours are sea are resolved by walking
outward across water to the nearest settled province. Twelve states finished
with no territory at all and were dropped rather than emitted as empty shells.

Result: **788 states covering all 10,623 land provinces, no gaps, no overlaps,
no duplicate ids, no sea or lake provinces inside a state.** Median 11 provinces
per state.

## Invariants

The generator fails rather than emitting a broken map. Every one of these is
checked on each run:

- every land province appears in exactly one state
- no province appears in two states
- no sea or lake province appears in any state
- no state has an empty province list
- no state id is defined twice
- every province referenced exists in `definition.csv`

These are the properties the previous mod violated. Checking them at generation
time rather than discovering the breach later is the whole point.

## What is still ahead

Geometry is settled; ownership is not. Every state still carries vanilla's 1936
owner, which for 1886 is wrong nearly everywhere — 129 states currently belong
to the Soviet Union, 72 to a Britain that in 1886 also holds Ireland, and
Czechoslovakia, Poland, Lithuania, Latvia and Estonia are Russian, German or
Austrian territory. Assigning 1886 owners and cores is the next body of work,
and it is research rather than engineering.

One question has to be answered before that starts: **granularity.** Vanilla's
states are drawn for 1936 politics and sometimes merge things 1886 keeps apart.
Thuringia is a single vanilla state; in 1886 it is eight separate duchies and
principalities. Weser-Ems is one state covering Oldenburg, Bremen and Prussian
Hanover, which are three different countries. The Palatinate is a detached piece
of Bavaria.

Splitting a vanilla state is legitimate and easy on this base — add rows to the
geometry table, move province ids between them, re-run, and the invariants
confirm the partition still holds. What is not acceptable is the previous
approach of adding the finer states *alongside* the coarse ones and leaving both
in place. Every split must remove the provinces from the parent in the same
edit, which the invariant check enforces automatically.

## Regenerating

`tools/data/definition_reference.csv` is committed so the tools can validate
without a game install. `provinces.bmp` is not — it is 34 MB and only needed to
rebuild adjacency. Recover it from history when required:

```
git show 1fc1d364:MOD/map/provinces.bmp > /tmp/provinces.bmp
python3 tools/province_adjacency.py tools/data/definition_reference.csv /tmp/provinces.bmp
```

Commit `1fc1d364` is an ancestor of `main` and holds the complete pre-reset
repository, so it can never be garbage collected.
