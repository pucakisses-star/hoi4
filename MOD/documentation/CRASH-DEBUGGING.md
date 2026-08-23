# Crash investigation

Eight crash reports, HOI4 1.19.2 "Operation Postern". Every one is
`EXCEPTION_ACCESS_VIOLATION`, and in all eight the faulting address ends in the
same 16 bits (`...F91B`). The high bits move because of ASLR; the offset does
not. That is one bug in one code path, not eight different problems.

The crash happens after script loading finishes. Every error below is
non-fatal - the game logs it and carries on - so the last line in `error.log`
is not the cause, it is just whatever finished last.

## What has been fixed and confirmed by the logs

| Fix | Result |
|---|---|
| 325 missing country tags restored | 900+ `Invalid effect 'PRS'` errors -> 0 |
| `set_politics{parties}` -> `set_popularities` | 195 deprecation warnings -> 0 |
| Vanilla ideology groups restored as a shim | ~211,000 errors -> 0 |
| Empty overrides for vanilla DLC on_actions | 393 -> 0 |
| Empty overrides for vanilla DLC events/focus/decisions | 3,140 -> 0 |
| 36 dead WW1-mod references in bookmarks | 36 -> 27 |

`error.log`: **250,685 -> 21,163 entries**. None of it stopped the crash.

## Why chasing the log stopped working

Each time the last-loaded vanilla directory was neutralised, the crash simply
moved to the next one: `on_actions` -> `events` -> `scripted_effects`. It is
following load order, not pointing at a culprit.

## The map is a genuine mess, but is probably not this bug

Worth recording, because it looks alarming and someone will find it again:

- **65 duplicate state ids.** 55 of those pairs cover completely different
  regions - `743-Belgrade.txt` against `743-Qingdao.txt`, `744-Baden.txt`
  against `744-Xian.txt`, `745-Dalian.txt` against `745-Oldenburg.txt`.
- **1,734 provinces belong to more than one state.** Only 479 of those involve
  a duplicate id; the other 1,255 are between states with perfectly valid,
  distinct ids - `10-Poland.txt` and `1313-Siedlce.txt` both claim province
  402, `1000-Indus Valley.txt` and `443-Hyderabad.txt` share four.

That is two overlapping state layouts, a coarse one and a fine-grained one,
both live. It should be fixed. But the game logs **no** complaint about states,
provinces, adjacencies or terrain in any of the eight runs, and the id ranges
do not separate the two layouts cleanly enough for a safe automatic fix, so it
is not currently the best explanation for the crash.

## What to do instead: bisect

Guessing has been exhausted. Renaming a directory inside the mod folder stops
the game loading it, which makes bisection cheap - one rename, one launch.

Four tests, in this order, each on a clean copy of the mod folder:

1. `history` -> `history_off`
2. `map` -> `map_off`
3. `common` -> `common_off`
4. `events` -> `events_off`

Whichever rename stops the crash contains the cause. Then bisect inside that
directory the same way - `common` in particular splits readily, since
`common/ideas`, `common/technologies`, `common/units` and `common/countries`
are each self-contained.

Expect the mod to look broken during these tests. That does not matter; the
only question being asked is whether it reaches the main menu.

## Two things worth checking first, since they are single launches

- Does **vanilla with no mods** launch? Establishes the game itself is sound.
- Does the mod launch with **every DLC disabled**? The idea-category
  replacement in `common/idea_tags/00_idea.txt` removes roughly 1,243 vanilla
  ideas, and the content that references them is overwhelmingly DLC content.
