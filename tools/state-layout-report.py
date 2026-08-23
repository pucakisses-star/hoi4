#!/usr/bin/env python3
"""
state-layout-report.py -- map out the two competing state layouts in
history/states/ and produce a worksheet for resolving them.

MOD/history/states/ contains two redraws of the same world stacked on top of
each other. They separate cleanly at state ID 800:

    IDs 1-800     coarse layout, ~12.6 provinces per state, the original world
    IDs 801+      fine layout,    ~3.4 provinces per state, a partial redraw
                                  that was never finished -- 80% of it sits on
                                  top of a coarse state nobody deleted

The obvious rule ("keep the fine state, delete the coarse one underneath")
resolves most of the overlap but is not free: the fine layer only redrew part
of each region, so deleting a coarse state drops any of its provinces that no
fine state picked up. Those are the "fall-through" provinces, and each one
needs assigning to some surviving state by hand.

This script quantifies that and writes a per-region worksheet.

Usage:
    python3 tools/state-layout-report.py [--mod MOD] [--boundary 800]
                                         [--out MOD/documentation/state-layout-worksheet.csv]
"""

import argparse
import collections
import csv
import os
import re
import sys

ID_RE = re.compile(r"\bid\s*=\s*(\d+)")
PROV_RE = re.compile(r"provinces\s*=\s*\{([^}]*)\}", re.S)


def load_provinces(mod):
    """province id -> terrain type, from map/definition.csv"""
    kinds = {}
    path = os.path.join(mod, "map", "definition.csv")
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            f = line.strip().split(";")
            if len(f) >= 5 and f[0].isdigit():
                kinds[int(f[0])] = f[4].strip().lower()
    kinds.pop(0, None)
    return kinds


def load_states(mod):
    """filename -> (state id, set of province ids)"""
    d = os.path.join(mod, "history", "states")
    states = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".txt"):
            continue
        text = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read()
        m = ID_RE.search(text)
        if not m:
            continue  # #OBSOLETE stubs and blanked files
        provs = {
            int(tok)
            for blk in PROV_RE.findall(text)
            for tok in blk.split()
            if tok.isdigit()
        }
        states[fn] = (int(m.group(1)), provs)
    return states


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mod", default="MOD")
    ap.add_argument("--boundary", type=int, default=800,
                    help="state IDs above this belong to the fine layout")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    kinds = load_provinces(args.mod)
    land = {p for p, k in kinds.items() if k == "land"}
    states = load_states(args.mod)
    if not states:
        sys.exit(f"no states parsed under {args.mod}/history/states")

    claims = collections.defaultdict(set)  # province -> {filename}
    for fn, (_, provs) in states.items():
        for p in provs:
            claims[p].add(fn)

    def is_fine(fn):
        return states[fn][0] > args.boundary

    # A coarse state is "contested" when it shares any province with a fine one.
    contested = {}
    for fn, (sid, provs) in states.items():
        if is_fine(fn):
            continue
        repl = sorted(
            {o for p in provs for o in claims[p] if o != fn and is_fine(o)},
            key=lambda x: states[x][0],
        )
        if repl:
            contested[fn] = repl

    survivors = set(states) - set(contested)
    kept_claims = set()
    for fn in survivors:
        kept_claims |= states[fn][1]

    rows = []
    all_fall = set()
    for fn, repl in contested.items():
        sid, provs = states[fn]
        fall = sorted((provs & land) - kept_claims)
        all_fall |= set(fall)
        taken = {p for r in repl for p in states[r][1]} & provs
        coverage = len(taken) / len(provs) if provs else 0.0
        kind = "replaced" if coverage >= 0.75 else (
            "carve-out" if coverage <= 0.35 else "mixed")
        rows.append({
            "kind": kind,
            "coarse_state": fn[:-4],
            "coarse_id": sid,
            "coarse_provinces": len(provs),
            "overlapped": len(taken),
            "coverage_pct": round(100 * coverage),
            "replacements": len(repl),
            "fall_through": len(fall),
            "replacement_states": " | ".join(r[:-4] for r in repl),
            "overlapped_provinces": " ".join(str(p) for p in sorted(taken)),
            "fall_through_provinces": " ".join(str(p) for p in fall),
            "decision": "",
        })
    order = {"replaced": 0, "mixed": 1, "carve-out": 2}
    rows.sort(key=lambda r: (order[r["kind"]], -r["fall_through"], -r["replacements"]))

    out = args.out or os.path.join(args.mod, "documentation", "state-layout-worksheet.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    coarse = [f for f in states if not is_fine(f)]
    fine = [f for f in states if is_fine(f)]

    def avg(g):
        return sum(len(states[f][1]) for f in g) / len(g) if g else 0

    now_double = sum(1 for v in claims.values() if len(v) > 1)
    after = collections.Counter()
    for fn in survivors:
        for p in states[fn][1]:
            after[p] += 1

    print(f"boundary: state ID {args.boundary}\n")
    print(f"  coarse (id <= {args.boundary}): {len(coarse):>4} states, "
          f"{avg(coarse):>4.1f} provinces each")
    print(f"  fine   (id >  {args.boundary}): {len(fine):>4} states, "
          f"{avg(fine):>4.1f} provinces each\n")
    print(f"  contested coarse states       {len(contested)}")
    print(f"  double-claimed provinces      {now_double} -> "
          f"{sum(1 for c in after.values() if c > 1)} if all are deleted")
    print(f"  land provinces with no state  {len(land - set(claims))} -> "
          f"{len(land - kept_claims)} if all are deleted")
    print(f"  fall-through to reassign      {len(all_fall)} distinct provinces")
    print(f"                                ({sum(r['fall_through'] for r in rows)} row entries; "
          f"a few provinces sit under two coarse states)\n")
    kinds = collections.Counter(r["kind"] for r in rows)
    print("  how the fine states relate to the coarse one underneath:")
    for k, desc in (("carve-out", "small state cut out of a bigger one; keep both"),
                    ("mixed",     "partial retiling; needs a look"),
                    ("replaced",  "coarse state fully retiled; delete it")):
        sel = [r for r in rows if r["kind"] == k]
        dbl = sum(r["overlapped"] for r in sel)
        print(f"    {k:<10} {kinds[k]:>4} regions  {dbl:>5} double-claimed provinces"
              f"  -- {desc}")
    print(f"\n  worksheet: {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
