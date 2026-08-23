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

## Locating provinces on the real world

Splitting a vanilla state along an 1886 border means knowing where its provinces
physically are, and the game gives them no coordinates — only a colour in a
bitmap. Three tools recover that.

`tools/province_adjacency.py` reads which provinces touch which, straight out of
`provinces.bmp`: 41,036 neighbour pairs, median six per province. No image
library is installed, and scanning 11.5 million pixels in a Python loop would be
slow, so boundaries are found by XORing each row against itself shifted one
pixel, collapsing the result to a 0/1 mask with `bytes.translate`, then walking
that with `bytes.find`. The loop runs once per boundary rather than once per
pixel; the whole map takes about a second.

`tools/province_geometry.py` gives each province a centroid and bounding box
using the same boundary positions to walk runs instead of pixels — every pixel
between two colour changes in a scanline belongs to one province. It accounts
for 100.00% of the bitmap.

`tools/map_projection.py` converts pixel coordinates to latitude and longitude.
The map is not a clean projection: longitude runs close to linear across the
full width, but latitude is stretched toward the poles and compressed in the far
south, badly enough that the Falklands sit north of Tasmania. No single global
formula fits, so the projection is fitted per region from anchor states whose
real position is known, as an affine transform — lat and lon each linear in x
and y, which absorbs the rotation and shear a plain scale cannot.

Fitted on 31 Central European anchors the residual is 45 km median, 119 km
worst. Some of that is the projection and some is the anchors, which are
eyeballed estimates of where a region's centre really is. It is not good enough
to place a border to the kilometre, and it does not need to be: an affine
transform preserves relative position, so which province lies north or west of
which is reliable even where the absolute figure drifts. That ordering is what
assigning provinces to states actually depends on.

## Does the province grid support 1886 Germany?

Yes, with one tight spot. Counting the vanilla states covering the 1886 German
Empire — including Posen, Pomerellen and Alsace-Lorraine, which vanilla assigns
to Poland and France but which were German in 1886 — gives **267 provinces for
26 member states**. Prussia takes roughly two thirds; the rest average about
three or four each, and even the smallest members can hold one.

The exception is Thuringia. Vanilla draws it as a single ten-province state. In
1886 that ground holds eight sovereign states — Saxe-Weimar-Eisenach,
Saxe-Meiningen, Saxe-Altenburg, Saxe-Coburg-Gotha, both Schwarzburgs and both
Reuss lines — plus Prussian Erfurt. Ten provinces can give each one province,
but the real duchies were interleaved with dozens of exclaves, and no province
grid at this resolution can reproduce that. The split will be a fair
approximation of who held what, not a reproduction of the map.

Two other vanilla states span countries and must be split rather than assigned
whole: Weser-Ems covers Oldenburg, Bremen and Prussian territory; Eastern Hesse
covers Prussian Hesse-Nassau, the Grand Duchy of Hesse and Frankfurt. Vanilla
has no Baden state at all — Baden sits inside its eighteen-province Württemberg,
which therefore has to be cut in three.

## The German Empire split

`tools/germany_1886.py` cuts the twenty-four vanilla states covering the Empire
into **fifty-two 1886 states**, one per country present in each. All twenty-six
Empire members end up holding territory.

| | provinces | | | provinces |
|---|---|---|---|---|
| Prussia | 166 | | Anhalt, Brunswick, Saxe-Meiningen, Saxe-Coburg and Gotha | 2 each |
| Bavaria | 35 | | Hamburg, Lübeck, Bremen, Mecklenburg-Strelitz | 1 each |
| Alsace-Lorraine, Württemberg | 9 | | Schaumburg-Lippe, Lippe, Waldeck-Pyrmont | 1 each |
| Baden | 8 | | Saxe-Weimar-Eisenach, Saxe-Altenburg | 1 each |
| Oldenburg, Mecklenburg-Schwerin, Saxony | 5 | | both Reuss lines, both Schwarzburgs | 1 each |
| Hesse | 4 | | | |

Every province was placed by converting its centroid to latitude and longitude
and comparing against where the 1886 border ran. Small fragments carry a note
naming the town they stand for, so the choice can be checked rather than taken
on trust. Some are very good — Saxe-Weimar's province sits 8 km from Weimar,
Saxe-Coburg-Gotha's 6 km from Gotha. Others are a compromise the grid forces.

Things worth knowing about the result:

- **Prussia is deliberately many states, not one.** It holds two thirds of the
  Empire across nineteen separate vanilla states, and keeping them separate is
  what makes Prussia feel like a federation's hegemon rather than a blob.
- **Some countries are deliberately discontiguous.** Oldenburg holds three
  blocks — Oldenburg proper, the Principality of Lübeck at Eutin, and Birkenfeld
  on the Nahe — because it really did. Saxe-Coburg and Gotha is two blocks,
  Coburg and Gotha, as it really was. Brunswick keeps its Blankenburg exclave.
- **Hohenzollern goes to Prussia**, not Württemberg. The dynasty's ancestral
  land was an exclave ruled from Berlin.
- **Alsace-Lorraine and Posen change hands from vanilla.** Vanilla assigns them
  to France and Poland; in 1886 both are German.
- **Thuringia is the honest compromise.** Eight sovereign states get one
  province each. The real duchies were interleaved with dozens of exclaves and
  no grid at this resolution reproduces that.

The generator refuses to write unless the split exactly reproduces the source
states: no province claimed twice, none left behind, and the total province
count unchanged before and after. That is the check the previous mod never had.

### A trap worth recording

The base table contains two different states both displaying as **Samara**, ids
251 and 401. An early version of this tool keyed states by display name, which
silently merged them and dropped nineteen provinces — and the per-state checks
still passed, because they only compared each source state against itself. The
loss only showed up in the whole-map coverage count.

Everything is keyed by state id now, `load_geometry` rejects a duplicate id
outright, and the tool refuses to write if the province total changes at all.
Display names are for humans; they are not identifiers.

## Austria-Hungary and the Balkans

The 1936 map barely resembles 1886 here. Yugoslavia and Czechoslovakia do not
exist and their ground is Habsburg or Ottoman; the Ottoman Empire still holds
Kosovo, Macedonia, Albania, Epirus and Thrace in Europe; Bosnia is Ottoman in
law and Austro-Hungarian in fact; Bessarabia is Russian.

Fifty-four vanilla states become sixty-two, giving **63 states and 544
provinces across 12 countries**:

| | states | provinces | | | states | provinces |
|---|---|---|---|---|---|---|
| Austria | 16 | 142 | | Bosnia | 1 | 30 |
| Hungary | 13 | 111 | | Greece | 4 | 29 |
| Ottoman Empire | 10 | 74 | | Russian Empire | 4 | 27 |
| Romania | 4 | 46 | | Serbia | 3 | 25 |
| Bulgaria | 4 | 37 | | Croatia-Slavonia | 2 | 13 |
| | | | | Montenegro | 1 | 5 |
| | | | | Crete | 1 | 5 |

Borders used, all as they stood in 1886:

- **Serbia's 1878 frontier**, south to roughly the latitude of Vranje. Kosovo
  and the Sandžak of Novi Pazar stayed Ottoman until 1912.
- **Montenegro's post-1878 borders** — Nikšić, Podgorica and Kolašin gained at
  Berlin, but Bijelo Polje and Pljevlja still Ottoman.
- **Greece's 1881 frontier**, bringing in Thessaly and Arta. Ioannina and Epirus
  remained Ottoman until 1913.
- **Bulgaria including Eastern Rumelia**, seized in September 1885 and accepted
  by the Porte at Tophane in April 1886 — but not the Rhodope and Kardzhali
  strip, which stayed Ottoman. Southern Dobruja is Bulgarian; Romania took only
  the northern half in 1878.
- **The Prut as the Romania–Russia border**, with Northern Dobruja Romanian and
  the Budjak Russian, both from the 1878 settlement.
- **Croatia-Slavonia** autonomous under Hungary, and the Croatian bank of the
  Sava separated from occupied Bosnia.

Two more source-data traps surfaced here. The state displaying as `East Galicia`
carries a **trailing space** in its game localisation, so a region table
addressing it by the name a human would write silently failed to find it; names
are stripped on load now. And the state named `Koinadugu` — a district of Sierra
Leone — actually sits in the **Danube delta**. As with `555-Lagos.txt` being the
Kuril Islands, the names in this data cannot be trusted; only the coordinates
can.

## Adding a region

`tools/build_1886_states.py` applies region tables in order to the recovered
geometry. A region is a module under `tools/regions/` supplying:

```python
SPLIT = {
    "<vanilla state name>": {"<1886 tag>": [province ids], ...},
    "<vanilla state name>": {"<1886 tag>": None},   # the whole state
}
NAMES = {"<tag>": "<display name>", ...}
```

`None` means every province of that state, which covers the common case where a
country simply inherits a vanilla state whole; an explicit list is only needed
where a state must be cut. Nothing is written unless every region reproduces its
sources exactly — nothing claimed twice, nothing left behind, map-wide province
total unchanged.
