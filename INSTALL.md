# Installing

Copy `MOD/` into your Hearts of Iron IV mod folder and create a `.mod` file
beside it that points at the copy.

```
Documents/Paradox Interactive/Hearts of Iron IV/mod/
    dsa/            <- the contents of MOD/
    dsa.mod         <- the file below
```

`dsa.mod`:

```
version="0.2"
tags={ "Alternative History" "Historical" "Map" }
name="Divided States of America"
supported_version="1.19.*"
replace_path="history/states"
path="C:/Users/<you>/Documents/Paradox Interactive/Hearts of Iron IV/mod/dsa"
```

Use forward slashes in `path`, even on Windows.

## replace_path belongs in this file

`replace_path` only takes effect in the outer `.mod` file that the launcher
reads — the one sitting next to the mod folder, not `descriptor.mod` inside it.
It is written in both here because the launcher regenerates `descriptor.mod`
from the outer file in some versions, but the outer file is the one that counts.

Two earlier test cycles were lost to exactly this: `replace_path` was set in
`descriptor.mod`, where it does nothing, and vanilla's directory kept loading.

## What replace_path does here

It makes the game ignore vanilla's `history/states` completely. This mod defines
all 857 states covering every one of the 10,623 land provinces, so nothing of
vanilla's is wanted. Without the declaration the game merges the two directories
by filename and every state id ends up defined twice.
