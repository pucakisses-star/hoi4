# tools

## build-mod.bat / build-mod.sh — assemble the mod one layer at a time

The mod is a merge of several others and does not currently reach the main
menu. Nine crash reports all show `EXCEPTION_ACCESS_VIOLATION` at the same
code offset, and every error in `error.log` is survivable — the fatal one is
not logged at all. Reading logs has not found it.

This builds the mod in stages instead. Each layer is a complete, loadable mod;
you launch after each one. The first layer that fails to reach the menu
contains the cause, and you are left holding a build that works.

**Windows:** double-click `build-mod.bat` and answer one question.
**macOS / Linux:** `./tools/build-mod.sh 3`

| Layer | Adds | Approx |
|---|---|---|
| 0 | descriptor only — baseline, does it load at all? | 1 MB |
| 1 | + `localisation` | 6 MB |
| 2 | + `gfx`, `interface`, `portraits`, `sound`, `music` | 833 MB |
| 3 | + `map`, `history` | 113 MB |
| 4 | + `common` (units, tech, characters, tags, on_actions) | 55 MB |
| 5 | + ideas, focus trees, decisions, bookmarks | 9 MB |
| 6 | + `events` — the complete mod | 4 MB |

Start at **3**. If it reaches the menu try **5**; if it crashes try **1**.
Three launches narrows the cause to a single layer.

It builds into a separate folder called `dsa-test` and **writes the `.mod`
descriptor itself**, so there is nothing to hand-edit. Your existing mods are
untouched. Enable "DSA test - layer N" in the launcher with every other mod
unchecked.

Layer 6 is verified byte-for-byte identical to the mod's loadable content
(16,919 files). Excluded deliberately: `important do not delete/` (another
mod's archive, which the game never reads), `documentation/`, `tests/`,
`tutorial/`, and `map/provinces.psd` (a Photoshop working file).

### Why the layers are grouped this way

`map` and `history` ride together because the mod ships its own
`definition.csv`; splitting them would leave vanilla state files pointing at
the mod's province IDs and produce a false result.

Bookmarks ride with ideas and focus trees for two reasons. The mod's bookmarks
reference specific ideas and focuses by name, and `blitzkrieg.txt` and
`the_gathering_storm.txt` are **empty stubs** that suppress vanilla's
bookmarks. Shipping the stubs without the mod's own bookmarks would leave the
game with no start dates at all.

## state-layout-report.py — map the two competing state layouts

See `MOD/documentation/MAP-LAYER-ANALYSIS.md`. Regenerates
`MOD/documentation/state-layout-worksheet.csv`.

```
python3 tools/state-layout-report.py [--boundary 800] [--mod MOD]
```

## shrink-repo.sh — rewrite history to drop bulk that need not be versioned

Dry-run by default; operates on a bare clone and prints the force-push commands
rather than running them. **Not yet run.** A full pass measured 721 MB → 222 MB.
Every existing clone must be re-cloned afterwards, so this needs a deliberate
go-ahead.
