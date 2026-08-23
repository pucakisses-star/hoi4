#!/usr/bin/env python3
"""
build_1886_states.py -- apply the 1886 region tables to the recovered state
geometry.

Reads tools/data/state_geometry.tsv, which holds vanilla's state shapes as one
partition of the land, and rewrites it region by region into the 1886 political
map. Each region module under tools/regions/ supplies a SPLIT table:

    SPLIT = {
        "<vanilla state name>": {"<1886 tag>": [province ids], ...},
        "<vanilla state name>": {"<1886 tag>": None},   # the whole state
    }

None means "every province of this state", for the common case where an 1886
country simply inherits a vanilla state whole. An explicit list is only needed
where a state has to be cut.

Nothing is written unless every region reproduces its source states exactly:
no province claimed twice, none left behind, and the map-wide province total
unchanged. That is the check the previous mod never had -- it added finer states
alongside the coarse ones they replaced and left both in place, which cost it
1,735 double-claimed provinces and, in the end, the ability to load at all.
"""

import argparse
import collections
import importlib
import os
import sys

REGIONS = ["germany", "balkans"]


def load_geometry(path):
    """Keyed by state id. Display names are not unique -- the base table holds
    two different states both called "Samara" -- so keying by name loses one."""
    rows = {}
    for i, line in enumerate(open(path, encoding="utf-8")):
        if i == 0:
            continue
        sid, key, name, cat, vo, provs = line.rstrip("\n").split("\t")
        # names come from game localisation and carry stray whitespace
        # ("East Galicia " has a trailing space); strip so region tables can
        # address states by the name a human would write.
        name = name.strip()
        sid = int(sid)
        if sid in rows:
            sys.exit(f"duplicate state id {sid} in {path}")
        rows[sid] = dict(id=sid, key=key, name=name, category=cat,
                         vanilla_owner=vo, provinces=[int(x) for x in provs.split()])
    return rows


def apply_region(geo, split, names, next_id, label):
    """Cut the named states per `split`. Returns (new geo, next free id, stats)."""
    idx = collections.defaultdict(list)
    for r in geo.values():
        idx[r["name"]].append(r)

    errs = []
    missing = [n for n in split if n not in idx]
    if missing:
        errs.append(f"{label}: source states not present: {missing}")
    ambiguous = [n for n in split if len(idx.get(n, [])) > 1]
    if ambiguous:
        errs.append(f"{label}: source state names not unique: {ambiguous}")
    if errs:
        return None, next_id, errs

    src_ids = {n: idx[n][0]["id"] for n in split}
    seen = collections.Counter()
    resolved = {}
    for name, parts in split.items():
        src = set(geo[src_ids[name]]["provinces"])
        # expand the None shorthand
        wildcard = [t for t, ps in parts.items() if ps is None]
        if len(wildcard) > 1:
            errs.append(f"{label}/{name}: more than one tag claims the whole state")
            continue
        explicit = []
        for t, ps in parts.items():
            if ps is not None:
                explicit.extend(ps)
        cs = set(explicit)
        if len(explicit) != len(cs):
            d = [p for p, n in collections.Counter(explicit).items() if n > 1]
            errs.append(f"{label}/{name}: province claimed twice: {d}")
        if cs - src:
            errs.append(f"{label}/{name}: claims provinces not in the state: {sorted(cs - src)}")
        parts_out = {t: list(ps) for t, ps in parts.items() if ps is not None}
        if wildcard:
            parts_out[wildcard[0]] = sorted(src - cs)
        elif src - cs:
            errs.append(f"{label}/{name}: leaves {len(src - cs)} provinces unassigned: "
                        f"{sorted(src - cs)}")
        resolved[name] = parts_out
        seen.update(p for ps in parts_out.values() for p in ps)

    across = [p for p, n in seen.items() if n > 1]
    if across:
        errs.append(f"{label}: provinces claimed by more than one source state: {across}")
    if errs:
        return None, next_id, errs

    split_ids = set(src_ids.values())
    out = {r["id"]: r for r in geo.values() if r["id"] not in split_ids}
    made = 0
    for name, parts in resolved.items():
        base = geo[src_ids[name]]
        order = sorted(parts.items(), key=lambda kv: -len(kv[1]))
        for i, (tag, ps) in enumerate(order):
            if not ps:
                continue
            if i == 0:
                sid, key = base["id"], base["key"]
                disp = base["name"] if len(order) == 1 else f"{base['name']} ({names[tag]})"
            else:
                sid, key = next_id, f"STATE_{next_id}"
                disp = f"{base['name']} ({names[tag]})"
                next_id += 1
            out[sid] = dict(id=sid, key=key, name=disp, category=base["category"],
                            vanilla_owner=tag, provinces=sorted(ps))
            made += 1
    return out, next_id, dict(sources=len(split), made=made)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--geometry", default="tools/data/state_geometry.tsv")
    ap.add_argument("--out", default="tools/data/state_geometry_1886.tsv")
    ap.add_argument("--regions", nargs="*", default=REGIONS)
    a = ap.parse_args()

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    geo = load_geometry(a.geometry)
    start_total = sum(len(r["provinces"]) for r in geo.values())
    next_id = max(geo) + 1
    print(f"base: {len(geo)} states, {start_total} provinces")

    per_tag = collections.Counter()
    for name in a.regions:
        mod = importlib.import_module(f"regions.{name}")
        new, next_id, res = apply_region(geo, mod.SPLIT, mod.NAMES, next_id, name)
        if new is None:
            for e in res:
                print("FAIL:", e)
            return 1
        total = sum(len(r["provinces"]) for r in new.values())
        if total != start_total:
            print(f"FAIL: {name} changed the province total {start_total} -> {total}")
            return 1
        geo = new
        print(f"  {name:<10} {res['sources']:>3} vanilla states -> {res['made']:>3} 1886 states")
        for t in mod.NAMES:
            per_tag[t] += sum(len(r["provinces"]) for r in geo.values()
                              if r["vanilla_owner"] == t)

    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("id\tkey\tname\tcategory\tvanilla_owner\tprovinces\n")
        for r in sorted(geo.values(), key=lambda r: r["id"]):
            fh.write(f"{r['id']}\t{r['key']}\t{r['name']}\t{r['category']}\t"
                     f"{r['vanilla_owner']}\t{' '.join(str(p) for p in r['provinces'])}\n")
    print(f"\nwrote {a.out}: {len(geo)} states, "
          f"{sum(len(r['provinces']) for r in geo.values())} provinces")
    return 0


if __name__ == "__main__":
    sys.exit(main())
