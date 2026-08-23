# Map layer analysis

Findings from a full validation sweep of `map/` and `history/states/`.
This is the layer that had never been reconciled after the mod merge.

## What was wrong

| Check | Before | After |
|---|---|---|
| States defined | 1327 | 1387 |
| Duplicate state IDs | 65 | **0** |
| Supply areas claiming a nonexistent state | 1 | **0** |
| Sea/lake provinces inside a land state | 108 | **0** |
| Land provinces belonging to no state | 329 | 168 |
| Provinces claimed by more than one state | 1735 | 1623 |
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
`history/states/`.

Display names for the 60 new states are in
`localisation/dsa_states_renumber_l_english.yml`, derived from their filenames.

**108 sea and lake provinces sitting inside land states.** `map/definition.csv`
types every province; states may only contain `land`. Finland alone claimed eight
sea provinces. Removed from all 73 affected files.

## Not fixed — needs a design decision

**1,623 provinces are still claimed by two different states**, across 555
distinct overlapping pairs involving 750 of the 1,387 state files. This is not a
set of typos. It is two different state layouts of the same world, both present:

```
375-Texas        <-> 1304-San Antonio    (11 provinces)
357-New England  <-> 961-Maine           (12 provinces)
276-Canada       <-> 1310-East Ontario   (11 provinces)
12-Latvia        <-> 1134 - Latgale      (11 provinces)
362-Virginia     <-> 746-West Virginia   (13 provinces)
286-Indochina    <-> 998-Cochinchina     (16 provinces)
```

One source drew Texas as a single state; another split it into provinces-level
regions. Both file sets were copied into `history/states/` and neither was
removed. The same is true across Europe, Africa, South America and Asia.

Resolving this means choosing, region by region, which granularity the mod wants
and deleting the other layout — then re-checking supply-area coverage. There is
no rule that picks correctly for you; it is a content decision, and it is the one
genuinely unfinished part of the mod.

The three source batches are distinguishable by filename convention and content
markers:

- `NNN - Name.txt` (spaces around the hyphen) — West Africa, Sierra Leone/Liberia
  districts, Orange Free State, Congo.
- `NNN-Name.txt` containing `state_culture_array` / `state_religion_array` —
  the Victorian base mod's own states.
- `NNN-Name.txt` containing 1930s dated blocks (`1938.10.25 = { controller = JAP }`)
  — unmodified vanilla Hearts of Iron IV state files that were copied back in on
  top of the mod's own.

**168 land provinces still belong to no state.** Most are the remainder of the
above; they will resolve as the layout question is settled.

## How to re-run these checks

Every number in this document comes from parsing `map/definition.csv` (province
id, type), `history/states/*.txt` (`id=`, `provinces={}`) and
`map/supplyareas/*.txt` (`states={}`) and cross-referencing them. The useful
invariants:

- every `id=` in `history/states/` is unique
- every province in a `provinces={}` block exists in `definition.csv` and is typed `land`
- every land province appears in exactly one `provinces={}` block
- every state id appears in exactly one supply area `states={}` block, and no supply area names a state that does not exist
- every province in `map/strategicregions/` exists and appears exactly once
