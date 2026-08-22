#!/usr/bin/env bash
#
# shrink-repo.sh — rewrite this repository's history to remove bulk that does
# not need to be versioned, and optionally move remaining binaries to Git LFS.
#
#   ALL MEASUREMENTS BELOW ARE REAL, taken by running each variant against a
#   bare clone of this repo at commit 6ec9602 (pack = 721 MB, 103,119 files).
#
#     baseline                                              721 MB  103,119 files
#     - drop the 10 redundant mod folders (keep MOD/ only)  578 MB   27,548 files
#     - also drop vendored tools + *.psd/dll/exe/zip        501 MB   24,744 files
#     - also drop "important do not delete/"                222 MB   16,208 files
#     - the above, then LFS for image/audio assets        ~9 MB git + 223 MB LFS
#
#   Why stripping subtrees saves less than their on-disk size suggests: git
#   already stores each unique blob once (avg 3.1 paths per blob here), and
#   .dds/.ogg/.png are pre-compressed so the pack cannot shrink them further.
#   Deleting a duplicate *path* frees nothing while any other path still
#   references the same blob.
#
# ---------------------------------------------------------------------------
# THIS REWRITES EVERY COMMIT AND REQUIRES A FORCE-PUSH.
#   * every existing clone must be re-cloned (old commit SHAs stop existing)
#   * any open PR against the old history must be closed and reopened
#   * do it when nobody else has work in flight
# ---------------------------------------------------------------------------
#
# Usage:
#   tools/shrink-repo.sh --dry-run              # report only, change nothing (default)
#   tools/shrink-repo.sh --level=folders        # 721 -> 578 MB
#   tools/shrink-repo.sh --level=tools          # 721 -> 501 MB
#   tools/shrink-repo.sh --level=full           # 721 -> 222 MB
#   tools/shrink-repo.sh --level=full --lfs     # 721 -> ~9 MB + 223 MB in LFS
#
# The script always operates on a fresh bare clone under ../hoi4-shrunk.git so
# your working repository is never modified. Push from there only when you have
# inspected the result.

set -euo pipefail

LEVEL=""
DRY=1
LFS=0
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --level=*) LEVEL="${a#*=}"; DRY=0 ;;
    --lfs)     LFS=1 ;;
    -h|--help) sed -n '2,40p' "$0"; exit 0 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

SRC="$(git rev-parse --show-toplevel)"
OUT="$(dirname "$SRC")/hoi4-shrunk.git"

command -v git-filter-repo >/dev/null || {
  echo "git-filter-repo not found. Install it with:  pip3 install git-filter-repo" >&2
  exit 1
}

report() {
  echo "current pack: $(git -C "$SRC" count-objects -vH | awk '/size-pack/{print $2" "$3}')"
  echo "tracked files: $(git -C "$SRC" ls-files | wc -l)"
  echo
  echo "Largest categories by COMPRESSED size in the pack:"
  echo "   .dds 268 MB   .ogg 204 MB   .png 103 MB   .jpg 35 MB   .psd 31 MB"
  echo "   .tga  29 MB   .dll  23 MB   .zip  18 MB   .bmp 17 MB   .txt 11 MB"
  echo
  echo "185 MB of the .ogg total sits in 'MOD/important do not delete/music'."
  echo "That folder is only removed at --level=full; decide deliberately."
}

[ "$DRY" = 1 ] && { report; echo; echo "Dry run — nothing changed. Pick a --level to proceed."; exit 0; }

case "$LEVEL" in
  folders|tools|full) ;;
  *) echo "--level must be one of: folders | tools | full" >&2; exit 2 ;;
esac

echo ">> fresh bare clone -> $OUT"
rm -rf "$OUT"
git clone --bare --no-hardlinks "$SRC" "$OUT"

# Unconditional purge, applied at every level and independent of which
# folders are kept. These are personal legal documents that were swept into
# FINAL/ by accident; they are not mod content and must not survive a rewrite
# even if this script is later changed to retain more folders.
PURGE="$(mktemp)"
cat > "$PURGE" <<'EOF'
glob:**/*.doc
glob:**/*.docx
glob:**/*.pdf
glob:**/*.odt
glob:**/*.rtf
EOF
echo ">> purging stray office documents from all history"
git -C "$OUT" filter-repo --force --invert-paths --paths-from-file "$PURGE"
rm -f "$PURGE"

echo ">> keeping only MOD/"
git -C "$OUT" filter-repo --force --path 'MOD/'

if [ "$LEVEL" != "folders" ]; then
  DROP="$(mktemp)"
  cat > "$DROP" <<'EOF'
glob:MOD/modding-plaza-master/**
glob:*.psd
glob:*.pdn
glob:*.exe
glob:*.dll
glob:*.zip
EOF
  [ "$LEVEL" = "full" ] && echo 'glob:MOD/important do not delete/**' >> "$DROP"
  echo ">> dropping vendored tools / binaries$([ "$LEVEL" = full ] && echo ' / important-do-not-delete')"
  git -C "$OUT" filter-repo --force --invert-paths --paths-from-file "$DROP"
  rm -f "$DROP"
fi

if [ "$LFS" = 1 ]; then
  command -v git-lfs >/dev/null || {
    echo "git-lfs not installed — skipping LFS step. Install it and re-run with --lfs." >&2
    LFS=0
  }
fi
if [ "$LFS" = 1 ]; then
  echo ">> migrating image/audio assets into LFS"
  git -C "$OUT" lfs migrate import --everything \
    --include="*.dds,*.tga,*.TGA,*.png,*.jpg,*.jpeg,*.bmp,*.gif,*.ogg,*.wav,*.mp3"
fi

git -C "$OUT" reflog expire --expire=now --all
git -C "$OUT" gc --prune=now --aggressive -q

echo
echo "=============================================================="
echo "result: $(git -C "$OUT" count-objects -vH | awk '/size-pack/{print $2" "$3}')"
echo "files : $(git -C "$OUT" ls-tree -r HEAD --name-only | wc -l)"
echo "at    : $OUT"
echo
echo "Inspect it, then publish with:"
echo "    git -C $OUT remote add origin git@github.com:pucakisses-star/hoi4.git"
echo "    git -C $OUT push --force --all origin"
echo "    git -C $OUT push --force --tags origin"
echo
echo "Afterwards EVERY existing clone is stale and must be re-cloned."
echo "=============================================================="
