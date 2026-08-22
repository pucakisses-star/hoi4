# Unintegrated Divided-States content

Salvaged from `FINAL2/` before the secondary mod folders were removed. **None
of this is wired into the mod** — it is kept here so it is not lost, and so
integrating it later is a deliberate decision rather than an archaeology
exercise.

## Why it was not simply copied into `common/`

**The focus trees would collide.** `MOD/common/national_focus/csa.txt` already
sets `country = COF`. Adding `COF_focus` from here would give the Confederacy
two focus trees — which is precisely the defect Onyyx recorded as note #23:

> "Both Confederate States of America_COF.txt and usa.txt focus tree files are
> set as focus tree for Confederates. I weighted the first one as more
> important."

`Texas_TEX.txt` has no counterpart in `MOD` and would not collide, but like the
others it references ideas, localisation and sprites that were written against
`FINAL2`, not against this mod. Dropping it into `common/` would introduce a
fresh set of dangling references immediately after those were cleaned up.

## Integrating any of it

1. Decide which COF tree wins — this one or `common/national_focus/csa.txt` —
   and delete or re-scope the loser. Two trees for one tag is the bug, not a
   feature.
2. Resolve every `focus = { id = ... }` icon against `interface/*.gfx`.
3. Resolve every idea and localisation key the tree references; the DSA
   localisation was salvaged separately into
   `localisation/dsa_salvaged_l_english.yml` and may already cover some.
4. Ideology tokens in these files use the pre-conversion vanilla set
   (`democratic`, `communism`, `fascism`, `neutrality`). This mod now uses the
   ten-group Victorian set, so they need the same mapping applied:
   democratic -> centrism, communism -> vanguard_communism,
   fascism -> chauvinist_populism, neutrality -> autocracy.

## These files are archived as-is, and five of them do not parse

`ideas_Aztlan.txt`, `ideas_Cascadia.txt` and `ideas_Confederacy.txt` are each
two closing braces short; `ideas_California.txt` and `ideas_Texas.txt` are one
short. Those defects came with the files from `FINAL2` and have deliberately
not been repaired, so that what is archived is what actually existed. Fix them
as part of integrating, not before — a file nobody loads does not benefit from
a speculative repair, and the imbalance is a useful signal about how finished
this content was.
