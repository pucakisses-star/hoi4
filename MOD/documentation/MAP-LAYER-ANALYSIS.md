# Map layer analysis

Findings from a full validation sweep of `map/` and `history/states/`.
This is the layer that had never been reconciled after the mod merge.

| Check | Before | After |
|---|---|---|
| States defined | 1327 | 1387 |
| Duplicate state IDs | 65 | **0** |
| Supply areas claiming a nonexistent state | 1 | **0** |
| Sea/lake provinces inside a land state | 108 | **0** |
| Provinces claimed by more than one state | 1735 | 1364 |
| Land provinces belonging to no state | 329 | 168 |
| Out-of-range province refs across `map/` + `history/` | 0 | 0 |
| Supply-area state coverage | 1327/1327 | 1387/1387 |

## Fixed

**`map/supplyareas/73-SupplyArea.txt` claimed state `8043`.** State IDs only go
up to 1327, so this was a lookup past the end of the state array. It was a stray
token — states 804 and 3 are both already claimed by other supply areas — so it
was simply removed. This was the only out-of-range numeric reference anywhere in
`map/` or `history/`.

**65 duplicate state IDs.** Two state files shared an ID; the game keeps one and
silently discards the other, orphaning the loser's provinces. Rather than delete
either, the discarded state was renumbered into free ID space (1328–1392) and
added to the same supply area as its former twin. Nothing references the new IDs
yet, so every existing script reference to the old ID still resolves to the same
state it resolved to before — the change is additive, not a behaviour change.

Which file kept the original ID was decided by how much territory it uniquely
owns (tiebreak: the one the game was already picking). Five of the movers turned
out to be exact regional duplicates with no unique provinces at all — those were
blanked with an `#OBSOLETE` marker, the convention already used elsewhere in
`history/states/`. Display names for the 60 new states are in
`localisation/dsa_states_renumber_l_english.yml`, derived from their filenames.

**108 sea and lake provinces sitting inside land states.** `map/definition.csv`
types every province; states may only contain `land`. Finland alone claimed eight
sea provinces. Removed from all 73 affected files.

**105 carve-out overlaps.** See below for what a carve-out is. The carved
provinces were removed from the parent state, and any victory point or
province-keyed `buildings` block sitting on them was moved into the state that
now owns them — Berlin's victory point to `951 - Berlin`, Moscow's to
`953 - Moscow`, New York City's dock buildings to `954 - New York City`. Victory
point and building-block totals are unchanged before and after (1131 and 556),
so nothing was dropped in the move. This resolved 259 double-claims and created
no new orphans.

## The two layouts

`history/states/` holds two redraws of the same world stacked on top of each
other. They separate cleanly at **state ID 800**:

| | states | provinces each | overlapping something |
|---|---|---|---|
| IDs 1–800 | 800 | 12.2 | 33% |
| IDs 801+ | 587 | 3.5 | 80% |

The high-ID batch is roughly 3.5× finer and 80% of it sits on top of a coarse
state that was never removed. It is not accidental duplication — it splits on
real historical lines: Taiwan by indigenous nation, South Africa by Boer republic
district, the Congo by precolonial kingdom, Japan by han, Texas by city. Someone
was systematically redrawing the world for the period and did not finish.

Three source batches are distinguishable by filename convention and content:

- `NNN - Name.txt` (spaces around the hyphen) — West Africa, Sierra Leone and
  Liberia districts, Orange Free State, Congo.
- `NNN-Name.txt` containing `state_culture_array` / `state_religion_array` —
  the Victorian base mod's own states.
- `NNN-Name.txt` containing 1930s dated blocks
  (`1938.10.25 = { controller = JAP }`) — unmodified vanilla Hearts of Iron IV
  state files that were copied back in on top of the mod's own.

Note that filenames are not reliable. `555-Lagos.txt` is the Kuril Islands
(`name="STATE_555" #Kuril Islands`, owner JAP). Read the file, not the name.

### Three kinds of overlap

Where a fine state overlaps a coarse one, the relationship is one of three
things, and the fix differs for each. `coverage` below means the share of the
coarse state's provinces that fine states have taken.

**Carve-out** (coverage ≤ 35%) — a small state cut out of a larger one:
`954 - New York City` out of `358-New York`, `951 - Berlin` out of
`64-Brandenburg`, `953 - Moscow` out of `219-Moscow Area`. Both states are
wanted; the parent simply never had the provinces removed from its list. This is
mechanical, needs no judgement, and has been applied — all 105 of them.

**Replaced** (coverage ≥ 75%) — the coarse state has been fully retiled and
should go:

```
375-Texas         49p  ->  6 states  (Amarillo, Comanche, TransPecos,
                                      San Antonio, Houston, Dallas-Fort Worth)
295-Congo         20p  ->  9 states  (Luba, Lunda, Kongo, Holo, Msiri, ...)
376-New Mexico    15p  ->  8 states  (Comanche, Navajo, South New Mexico, ...)
231-Georgia       18p  ->  7 states  (Abkhazeti, Guria, Samegrelo, Svaneti, ...)
524-Taiwan        10p  ->  6 states  (Atayal, Amis, Rukai, Paiwan, ...)
```

**Mixed** (35–75%) — partially retiled. The threshold between mixed and carve-out
is arbitrary; the distribution is smooth across it, and cases just above the line
(`69-Sudatenland` at 36%, keeping 9 of 14 provinces) read like carve-outs too.
Widening the cutoff would resolve more automatically, at the cost of leaving
some half-replaced states in place.

## What remains

**1,364 provinces are still claimed by two states**, across 134 contested coarse
states — 99 mixed, 35 replaced.

Deleting every remaining contested coarse state would drop double-claims to 200,
but it is not free: it would orphan **690 land provinces** that no fine state
picked up, because the fine layer only redrew part of each region. Texas is the
mild case — 49 provinces down to 44. Those 690 need reassigning to a surviving
state by hand.

So the remaining work is one rule plus a reassignment pass, not 134 independent
judgement calls. The 168 land provinces already without a state are the tail of
the same question.

`documentation/state-layout-worksheet.csv` has one row per contested state:
its ID, how many provinces it owns, how many were taken and by which states, the
coverage percentage, the exact province IDs that would fall through, and a blank
`decision` column. Sorted worst-first.

Regenerate it after any change with:

```
python3 tools/state-layout-report.py
```

`--boundary` moves the ID split (default 800) and `--mod` points at a different
mod folder.

## Invariants

Every number here comes from parsing `map/definition.csv` (province id, type),
`history/states/*.txt` (`id=`, `provinces={}`), `map/supplyareas/*.txt`
(`states={}`) and `map/strategicregions/*.txt`. The properties worth re-checking
after any map edit:

- every `id=` in `history/states/` is unique
- every province in a `provinces={}` block exists in `definition.csv` and is typed `land`
- every land province appears in exactly one `provinces={}` block
- no state is left with an empty province list
- every state id appears in exactly one supply area `states={}` block, and no supply area names a state that does not exist
- every province in `map/strategicregions/` exists and appears exactly once
- victory points and province-keyed `buildings` entries sit on a province the state actually owns
