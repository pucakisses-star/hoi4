# Installing this mod

`MOD/` in this repository is the mod itself. Its **contents** go into a folder
under the game's mod directory, and a second `.mod` file sits beside that folder
pointing at it. HOI4 will not show the mod in the launcher without that second
file — this is the step that most often goes wrong.

## Layout the game expects

    Documents/Paradox Interactive/Hearts of Iron IV/mod/
    |
    +-- dsa.mod        <- outer descriptor. MUST contain a path= line.
    |
    +-- dsa/           <- the contents of this repository's MOD/ folder
        +-- descriptor.mod
        +-- common/  events/  history/  gfx/
        +-- interface/  localisation/  map/  music/
        +-- portraits/  sound/  tutorial/

The inner `descriptor.mod` and the outer `dsa.mod` are near-identical. The
difference is that only the outer one carries `path=`, and only the outer one
is what the launcher reads.

## Steps

1. Create the folder `.../Hearts of Iron IV/mod/dsa/`.
2. Copy everything inside this repository's `MOD/` folder into it.
3. Copy `dsa.mod` from this repository's root into
   `.../Hearts of Iron IV/mod/` — beside the `dsa` folder, not inside it.
4. Open `dsa.mod` and set `path=` to the real absolute location of the folder
   from step 1, using forward slashes even on Windows.
5. Launch, and enable the mod in the launcher's Playsets.

## What not to copy

Four directories in `MOD/` are not mod content and the game ignores them.
Leaving them out keeps the install about 1.1 GB smaller:

  - `modding-plaza-master/`      591 MB, third-party tool suite
  - `important do not delete/`   522 MB, another mod's archive plus a backup
  - `documentation/`             notes, and content not yet integrated
  - `tests/`                     scripted test bundles

`tools/` at the repository root is likewise repo tooling, not mod content.

The game only reads these directories: `common`, `events`, `history`, `gfx`,
`interface`, `localisation`, `map`, `music`, `portraits`, `sound`, `tutorial` -
plus `descriptor.mod` and `thumbnail.png`.

## supported_version

`descriptor.mod` currently declares `supported_version="1.16.*"`. Set it to the
build actually installed. It is advisory - a mismatch only produces a launcher
warning and does not stop the mod loading.
