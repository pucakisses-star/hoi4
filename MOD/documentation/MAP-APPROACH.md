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

## The rest of Europe

225 states, almost all whole-state inheritance — the borders of France, Iberia,
Italy, the Low Countries and Scandinavia in 1886 are close enough to 1936 that
vanilla's states carry over unchanged. What changes is ownership in the east and
north-west:

| | states | provinces | |
|---|---|---|---|
| Russian Empire | 111 | 1989 | Congress Poland, the Baltic governorates, Belarus, Ukraine, the Caucasus |
| France | 28 | 282 | Third Republic; Alsace-Lorraine already German |
| Spain | 16 | 222 | Restoration monarchy; Alfonso XIII born May 1886 |
| United Kingdom | 22 | 150 | **including all of Ireland** — no partition until 1922 |
| Italy | 12 | 124 | unified since 1870; the Pope holds no territory |
| Sweden | 7 | 201 | |
| Finland | 8 | 155 | Russian Grand Duchy, own diet, currency and army |
| Norway | 4 | 135 | personal union with Sweden, separate kingdom |
| Portugal, Denmark, Netherlands, Belgium, Switzerland, Luxembourg | 17 | 121 | Denmark including Iceland and the Faroes |

Poland, Lithuania, Latvia, Estonia, Belarus and Ukraine are not countries in
1886 — they are governorates. Ireland is not one either. Finland and Norway keep
their tags as genuine autonomous or personal-union subjects, the same case as
Croatia-Slavonia under Hungary.

**Anatolia and Mosul are deliberately excluded.** They are Ottoman, but Russia
took Kars, Ardahan and Batumi in 1878, and carving those out needs a Caucasus
projection fit — the Central European one is unreliable that far east. Left for
a Near East region rather than assigned to a border known to be wrong.

Running total: **5,228 of 10,623 provinces (49%) on 1886 owners, across 459
states.**

### Names are still not identifiers

The base data contains two adjacent Volga states **both named "Samara"** (ids
251 and 401). The driver refused to write rather than guess, which is the
behaviour wanted. Region tables can now address a state as `"Name#id"` when the
name alone is ambiguous, and the driver checks that the id really does carry
that name.

A second hazard surfaced in the same place. Python collapses duplicate keys in a
dict literal silently, so a region table can lose an entry with no error at all
— the generated Europe table briefly had `"Samara#251"` twice. The driver now
parses each region module with `ast` and rejects duplicate keys in `SPLIT`
before using it. Verified by deliberately introducing one.

## The Near East, and a correction

Fifty vanilla states become fifty-two. The extra two are the point of the
region: **Russia took Kars, Ardahan and Batumi from the Ottomans at Berlin in
1878** and held them until 1918. The Europe pass left all of Anatolia Ottoman
because the Central European projection is unreliable that far east and guessing
the salient would have been worse than deferring it. Fitted on thirty Near
Eastern anchors instead, the provinces are identifiable, and Trabzon and Erzurum
are now cut — five provinces to Russia, sixteen left Ottoman.

Everything else here is 1886 rather than 1936:

- **Syria, Palestine and Transjordan are Ottoman provinces.** There are no
  mandates until after 1918.
- **Mount Lebanon keeps its own tag** — an autonomous mutasarrifate with a
  Christian governor guaranteed by the powers after the 1860 massacres.
- **Egypt is Egyptian**, a Khedivate under Ottoman suzerainty, occupied by
  Britain since 1882 but not annexed.
- **Sudan is not Egyptian at all.** The Mahdists took Khartoum in January 1885
  and hold it until Omdurman in 1898.
- **Central Arabia belongs to the Rashidi of Ha'il**, not the Saudis, whose
  second state is a rump extinguished in 1891.
- **Yemen is Ottoman**; Aden has been British since 1839.

### Two defects this pass exposed

**Lebanon and Tunisia had been swept into Europe.** The Europe table was
generated by taking every state inside a latitude/longitude box — and that box
was computed with the Central European projection, which is badly wrong at their
longitude. The result put Mount Lebanon under France thirty-four years before
the mandate. Regions are no longer defined by a projection box: a state is in a
region because it is listed in that region's table, by name, and nothing else.

**The coverage figure was overstated.** Progress was being measured by asking
whether a state's owner tag looked like an 1886 owner, which silently counted
115 colonial states — 1,018 provinces — as converted merely because they still
carried the tag of a European colonial power that no region had ever touched.
Some of those are wrong for 1886 anyway: Libya is not Italian until 1911, and
the Congo is Leopold II's personal property rather than Belgian until 1908.

The geometry table now carries an **`assigned_by`** column naming the region
that set each state's owner, and coverage counts only states carrying that
stamp. The reported figure went from an inferred 49% to a measured **44%**, which
is the real one. A number derived from a proxy was quietly wrong; a number
derived from a record of what actually happened cannot be.

Running total: **4,675 of 10,623 provinces (44%) across 389 states.**

## Asia

141 vanilla states become 142, giving **142 states and 2,148 provinces across 16
countries**. The map goes from 44% converted to **64%**.

| | states | provinces | | | states | provinces |
|---|---|---|---|---|---|---|
| Qing Empire | 56 | 970 | | Dai Nam | 1 | 29 |
| Russian Empire | 35 | 583 | | Cambodia | 1 | 27 |
| Japan | 14 | 125 | | Luang Prabang | 1 | 26 |
| Spain | 10 | 93 | | Tibet | 3 | 24 |
| Siam | 2 | 82 | | United Kingdom | 8 | 19 |
| Korea | 2 | 70 | | Champasak | 1 | 13 |
| France / Afghanistan | 2 each | 38 / 33 | | Prussia / Portugal | 1 / 3 | 9 / 7 |

The big correction is the one the country list already makes: **CHI is the
Republic, and in 1886 there is no republic.** The Qing hold everything from the
Amur to Hainan as one country — China proper, Manchuria, Inner and Outer
Mongolia, Tannu Uriankhai, Xinjiang (a province since 1884), Taiwan (until
1895), Dalian (until 1898) and Guangzhouwan (until 1898). Vanilla scatters that
across eleven tags.

Others worth naming:

- **Korea is Joseon**, independent under Qing suzerainty. Japan does not annex
  it until 1910.
- **Sakhalin is entirely Russian and the Kurils entirely Japanese**, under the
  Treaty of Saint Petersburg of 1875.
- **The Philippines, Carolines, Palau and Marianas are Spanish.** The United
  States does not appear in the Pacific until 1898.
- **The Marshall Islands are a German protectorate** from 1885. The Empire's
  colonies belong to the Empire, so Prussia stands in for it as the seat of the
  Kaiser — a modelling choice, not a historical claim.
- **Laos is not French until 1893.** It is two Siamese vassal kingdoms, split
  here at 17.5°N: 26 provinces to Luang Prabang, 13 to Champasak. The Vientiane
  region, destroyed by Siam in 1828 and administered directly since, is folded
  into Luang Prabang.
- **Tibet keeps its tag** — Qing suzerainty, but self-governing.

### The naming problem, finally characterised

Fourteen states in this region carry names describing somewhere else entirely:
state 744 holds Xian's provinces under the name **"Baden"**, 751 is Liangshan
called **"Roma"**, 750 is Changde called **"South Kuril Islands"**, 761 is
Hulunbuir called **"Man"**.

The cause is now understood. These are all in the id range 743–796 where two
state layouts collided. The source mod renumbered vanilla's states and rewrote
the localisation to match *its* layout, but the provinces that survived the
collision came from the other one. So the name describes the discarded state and
the provinces describe the surviving one.

An attempt to fix this by preferring the filename over the localisation made
things worse and was reverted: state 743 holds the Banat, its localisation
correctly says "West Banat", and its **filename** says "Belgrade". Neither source
is reliably right — which one lies varies per state, depending on which file won
the collision.

Both names are now recorded in the geometry builder, neither is trusted, and
region tables note the real identity beside each misleading entry. Where a name
is ambiguous rather than merely wrong, tables address the state as `"Name#id"`.

## The Americas

148 states, 1,786 provinces. The map goes from 64% to **81%** converted.

**North America stays divided — and that is a design decision, not history.**
The recovered geometry carries a fully worked-out alternate United States from
the previous mod, and since the mod is named for it, it is preserved rather than
overwritten with a single historical USA:

| | states | provinces |
|---|---|---|
| United States | 28 | 458 |
| Confederate States | 11 | 186 |
| California | 1 | 59 |
| Texas | 1 | 50 |
| Cascadia (Washington, Oregon) | 2 | 41 |
| Aztec (New Mexico, Arizona) | 2 | 32 |
| Deseret (Utah) | 1 | 13 |

Nothing here asserts that is history. It is the author's to change; the point is
that it was not silently destroyed.

The genuine 1886 corrections:

- **Cuba and Puerto Rico are Spanish.** The United States takes them in 1898.
- **Panama is Colombian** — the isthmus and the canal zone both — until 1903.
- **Hawaii is an independent kingdom** under Kalākaua, annexed only in 1898.
- **Samoa is a contested independent kingdom**, not a New Zealand possession.
- **Newfoundland and Labrador are a separate British colony.** Canada is a
  self-governing Dominion, as it has been since 1867.

Everything else is whole-state inheritance: every Latin American republic
existed by 1886 with borders close enough to 1936 to carry over. Brazil is an
empire under Pedro II until 1889, but the tag is unchanged.

## A tag collision that had already happened

Assigning Prussia the tag `PRU` was wrong: **vanilla uses `PRU` for Peru**, and
the recovered geometry has five Peruvian states under it. Prussia is now `PRS`.

The collision got through because the guard was a **hand-written list** of what
vanilla tags supposedly were. Checked against the tags the data actually uses,
that list was missing twenty-six of them — `PRU` among them, along with `TEX`,
`CAL`, `DES`, `AZT` and the rest of the previous mod's alternate America. The
guard now reads the geometry and takes the union with the written list, so a tag
already in use cannot be claimed by accident.

Four tags remain shared, and all four are agreement rather than collision:
`DAH` Dahomey, `NKO` Nkore, `OFS` Orange Free State and `RUS` Russian Empire
were coined independently and identically by the previous mod and by this
country list. Those are recorded as known-benign so they stop being reported.

Running total: **8,609 of 10,623 provinces (81%) across 679 states.**

## India, Australasia, the Indies, Africa — and completion

The map is now **100% converted: 857 states, 174 countries, all 10,623 land
provinces**, every invariant clean.

**India.** Vanilla draws British India as one country. In 1886 roughly two
fifths of the subcontinent by area was ruled by princes with their own courts,
armies and coinage — Hyderabad alone was larger than Italy. The larger states
are separated out; the hundreds of small ones are not, because the province grid
cannot carry them. Rajputana is divided between Bikaner, Jaipur, Jodhpur and
Udaipur; Gujarat between Kutch, Junagadh, Baroda and British Surat.

The South Asian projection is the worst of any region — **112 km median
residual** — so these splits use *relative* position within each state rather
than absolute coordinates: Bikaner is Rajputana's north-western corner, Udaipur
its southern. That ordering survives the distortion even where the numbers do
not.

**Australia is not a country.** Federation is fifteen years away. In 1886 there
are six separate self-governing colonies with their own parliaments, tariffs,
postage and rail gauges — trains could not cross from New South Wales to
Victoria without passengers changing carriage. Six new tags. New Guinea is
divided three ways in 1884–85 and none of them is Australian: Dutch west,
German north-east, British south-east, the last after Queensland tried to annex
it unilaterally and London disallowed it.

**The Indies.** Every Malay sultanate separately sovereign, Bali as five
kingdoms, Aceh thirteen years into a war with the Dutch with eighteen still to
run, and Borneo split between a Sultan, an English dynasty ruling Sarawak as
rajahs, and a chartered company.

**Africa — the year after Berlin**, when the partition was agreed on paper and
had barely begun on the ground. This is where vanilla is most misleading:

| Vanilla says | 1886 says |
|---|---|
| Italian Libya | **Ottoman** — Italy invades in 1911 |
| Belgian Congo | **Leopold II's personal property** — not Belgian until 1908 |
| British Sudan | **the Mahdists** — they hold Khartoum until 1898 |
| British Kenya | **the Sultan of Zanzibar's coast** |
| British Uganda | **the Kingdom of Buganda** |
| British Tanganyika | **German** — chartered 1885 |
| British Rhodesia | **Lobengula's Ndebele kingdom** — Rhodes arrives in 1890 |
| French Morocco | **an independent sultanate** until 1912 |
| Italian Somaliland | **the Majeerteen Sultanate** — Italy arrives in 1889 |
| South Africa | **the Transvaal, the Orange Free State, the Cape, Natal** |

Assigning any of those to its 1936 owner would put a colony on the map
twenty-five years early.

Much of Africa needed no correction. The previous mod had already built Ashanti,
Dahomey, the Mossi, the Aro, the Kru, Kong, the Toucouleur, Wadai, the Sotho and
the Orange Free State as real polities with territory. That work was
1886-appropriate and is kept; only the colonial layer on top of it was wrong.

**The tail.** Twenty-nine states were already on correct owners but had never
been stamped by a region, so they were invisible to the coverage count. They are
stamped now after checking, and four of them turned out to be wrong: **Guam** was
Spanish until 1898, **Setsoto** is in Basutoland rather than France, **Anziku** is
a Congo kingdom rather than Spanish, and **Port-de-Paix** is in Haiti — Spain's
half of Hispaniola had been the Dominican Republic since 1865.

That is the `assigned_by` column earning its place. Under the old
count-by-owner-tag method all twenty-nine would have been silently counted as
converted, and those four errors would have shipped.
