#!/usr/bin/env bash
#
# build-mod.sh -- assemble the mod one layer at a time (macOS / Linux).
# Windows users: double-click tools\build-mod.bat instead.
#
# Each layer is a mod that loads on its own, so you can launch after every
# step. Whichever layer first fails to reach the main menu contains the cause.
#
#   ./tools/build-mod.sh 3              build layer 3 into the game's mod dir
#   ./tools/build-mod.sh 3 --dry-run    just print what layer 3 contains
#   ./tools/build-mod.sh 3 --dest DIR   build somewhere else
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/../MOD"
LEVEL="${1:-}"
shift || true
DRY=0; DEST=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --dest) DEST="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

case "$LEVEL" in
  0|1|2|3|4|5|6) ;;
  *) cat >&2 <<USAGE
usage: $(basename "$0") <0-6> [--dry-run] [--dest DIR]

  0   descriptor only  (baseline: does it load?)        1 MB
  1   + localisation                                    6 MB
  2   + gfx, interface, portraits, sound, music       833 MB
  3   + map, history                                  113 MB
  4   + common (units, tech, characters, tags)         55 MB
  5   + ideas, focus trees, decisions, bookmarks        9 MB
  6   + events              (= the complete mod)        4 MB

Start at 3. Loads -> try 5. Crashes -> try 1. Three launches isolates it.
USAGE
     exit 2 ;;
esac

[ -f "$SRC/descriptor.mod" ] || { echo "no MOD folder at $SRC" >&2; exit 1; }

# layer N -> the paths it adds, relative to MOD/
layer_paths() {
  case "$1" in
    0) echo "descriptor.mod thumbnail.png" ;;
    1) echo "localisation" ;;
    2) echo "gfx interface portraits sound music" ;;
    3) echo "map history" ;;
    4) echo "common" ;;
    5) echo "common/ideas common/national_focus common/decisions common/bookmarks" ;;
    6) echo "events" ;;
  esac
}
# directories held back at layer 4 and released at layer 5
HOLDBACK="ideas national_focus decisions bookmarks"

if [ "$DRY" = 1 ]; then
  echo "layer $LEVEL would contain:"
  for l in $(seq 0 "$LEVEL"); do
    for p in $(layer_paths "$l"); do
      [ -e "$SRC/$p" ] || continue
      if [ "$l" = 4 ]; then
        printf '  %-46s %s\n' "common/*.txt (loose files)" \
          "$(find "$SRC/common" -maxdepth 1 -type f | wc -l | tr -d ' ') files"
        for d in "$SRC/common"/*/; do
          b="$(basename "$d")"
          case " $HOLDBACK " in *" $b "*) continue ;; esac
          printf '  %-46s %s\n' "common/$b" "$(du -sh "$d" | cut -f1)"
        done
      else
        printf '  %-46s %s\n' "$p" "$(du -sh "$SRC/$p" 2>/dev/null | cut -f1)"
      fi
    done
  done
  exit 0
fi

if [ -z "$DEST" ]; then
  for cand in \
    "$HOME/Documents/Paradox Interactive/Hearts of Iron IV/mod" \
    "$HOME/.local/share/Paradox Interactive/Hearts of Iron IV/mod"; do
    [ -d "$cand" ] && { MODDIR="$cand"; break; }
  done
  [ -n "${MODDIR:-}" ] || { echo "could not find the HOI4 mod folder; pass --dest" >&2; exit 1; }
  DEST="$MODDIR/dsa-test"
else
  MODDIR="$(dirname "$DEST")"
fi

echo "clearing $DEST"
rm -rf "$DEST"; mkdir -p "$DEST"

copy() { # copy() <relative path>
  local p="$1"
  [ -e "$SRC/$p" ] || return 0
  mkdir -p "$(dirname "$DEST/$p")"
  if [ -d "$SRC/$p" ]; then
    mkdir -p "$DEST/$p"
    cp -a "$SRC/$p/." "$DEST/$p/"
    # Photoshop working file; the game never reads it
    rm -f "$DEST/$p/provinces.psd"
  else
    cp "$SRC/$p" "$DEST/$p"
  fi
}

for l in $(seq 0 "$LEVEL"); do
  echo "  layer $l"
  if [ "$l" = 4 ]; then
    mkdir -p "$DEST/common"
    # loose .txt files sitting directly in common/ (combat_tactics, weather, ...)
    find "$SRC/common" -maxdepth 1 -type f -exec cp {} "$DEST/common/" \;
    for d in "$SRC/common"/*/; do
      b="$(basename "$d")"
      case " $HOLDBACK " in *" $b "*) continue ;; esac
      copy "common/$b"
    done
  else
    for p in $(layer_paths "$l"); do copy "$p"; done
  fi
done

NAME="DSA test - layer $LEVEL"
{
  echo "version=\"1.3\""
  echo "name=\"$NAME\""
  echo "supported_version=\"1.19.*\""
  [ "$LEVEL" -ge 4 ] && echo "replace_path=\"common/on_actions\""
} > "$DEST/descriptor.mod"
{
  cat "$DEST/descriptor.mod"
  echo "path=\"$DEST\""
} > "$MODDIR/dsa-test.mod"

echo
echo "built layer $LEVEL at $DEST"
echo "enable \"$NAME\" in the launcher with every other mod unchecked, then Play."
echo "reached the menu -> rerun with a HIGHER number; crashed -> LOWER."
