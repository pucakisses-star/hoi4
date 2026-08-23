#!/usr/bin/env python3
"""
build_state_geometry.py -- recover a clean, complete state geometry for the map.

The previous mod's history/states held two layouts stacked on each other. The
low band (ids 1-800) is vanilla Hearts of Iron IV's own state geometry, still
intact: 800 states, no duplicate ids. The band above 800 was a partial finer
redraw that took provinces out of the vanilla states without deleting them, so
the low band alone is 119 provinces double-claimed and 949 land provinces short
of complete.

This repairs it into a partition -- every land province in exactly one state,
no province in two. Both defects are fixed by the same rule: a province belongs
to the state that owns most of the provinces it physically touches, using the
adjacency graph read out of provinces.bmp. Orphans are resolved by repeated
passes, because an orphan's neighbours may themselves be orphans; each pass
only assigns provinces that currently touch a decided state, so the frontier
grows inward from known territory.

Output is one tab-separated table: the single source of truth for state shape.
Ownership for 1886 is a separate concern and lives elsewhere.
"""

import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from province_adjacency import load_definition, adjacency

ID = re.compile(r"\bid\s*=\s*(\d+)")
NAME = re.compile(r'\bname\s*=\s*"([^"]+)"')
CAT = re.compile(r"\bstate_category\s*=\s*(\w+)")
OWNER = re.compile(r"\bowner\s*=\s*([A-Z0-9]{3})")
PROV = re.compile(r"provinces\s*=\s*\{([^}]*)\}", re.S)


def load_states(d, max_id):
    out = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".txt"):
            continue
        t = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read()
        m = ID.search(t)
        if not m:
            continue
        sid = int(m.group(1))
        if sid > max_id:
            continue
        provs = {int(x) for blk in PROV.findall(t) for x in blk.split() if x.isdigit()}
        nm, cat, ow = NAME.search(t), CAT.search(t), OWNER.search(t)
        out[sid] = dict(
            id=sid,
            name=nm.group(1) if nm else f"STATE_{sid}",
            category=cat.group(1) if cat else "rural",
            vanilla_owner=ow.group(1) if ow else "",
            provinces=provs,
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", required=True, help="reference history/states directory")
    ap.add_argument("--definition", required=True)
    ap.add_argument("--bmp", required=True)
    ap.add_argument("--max-id", type=int, default=800)
    ap.add_argument("--names", help="localisation yml supplying STATE_<n> display names")
    ap.add_argument("--out", default="tools/data/state_geometry.tsv")
    a = ap.parse_args()

    names = {}
    if a.names:
        for line in open(a.names, encoding="utf-8-sig", errors="replace"):
            m = re.match(r'\s*(STATE_\d+):\d*\s*"(.*)"\s*$', line)
            if m:
                names[m.group(1)] = m.group(2)
        print(f"loaded {len(names)} state display names")

    rgb2id, kind = load_definition(a.definition)
    land = {p for p, k in kind.items() if k == "land"}
    land.discard(0)
    adj, _unknown, _dims = adjacency(a.bmp, rgb2id)
    states = load_states(a.states, a.max_id)
    print(f"loaded {len(states)} states, {len(land)} land provinces")

    owner = {}
    contested = collections.defaultdict(list)
    for sid, s in states.items():
        for p in s["provinces"]:
            if p in owner:
                contested[p].append(sid)
            else:
                owner[p] = sid
    for p in list(contested):
        contested[p].insert(0, owner[p])

    # drop anything that is not land: sea and lake provinces are never in a state
    dropped = [p for p in list(owner) if p not in land]
    for p in dropped:
        del owner[p]
    print(f"removed {len(dropped)} non-land provinces claimed by a state")

    def best_state(p, candidates=None):
        """the state owning most of p's physical neighbours"""
        votes = collections.Counter()
        for n in adj.get(p, ()):
            s = owner.get(n)
            if s is not None and (candidates is None or s in candidates):
                votes[s] += 1
        return votes.most_common(1)[0][0] if votes else None

    fixed = 0
    for p, cands in contested.items():
        if p not in land:
            continue
        pick = best_state(p, set(cands)) or cands[0]
        owner[p] = pick
        fixed += 1
    print(f"resolved {fixed} double-claimed provinces by neighbour majority")

    missing = land - set(owner)
    print(f"land provinces with no state: {len(missing)}")
    rounds = 0
    while missing:
        assigned = {}
        for p in missing:
            s = best_state(p)
            if s is not None:
                assigned[p] = s
        if not assigned:
            # islands: every neighbour is sea, so no land vote ever arrives.
            # Walk outward through water to the nearest province that has a state.
            for p in sorted(missing):
                seen, frontier = {p}, [p]
                found = None
                while frontier and found is None:
                    nxt = []
                    for q in frontier:
                        for n in adj.get(q, ()):
                            if n in seen:
                                continue
                            seen.add(n)
                            if n in owner:
                                found = owner[n]
                                break
                            nxt.append(n)
                        if found is not None:
                            break
                    frontier = nxt
                if found is not None:
                    assigned[p] = found
            if assigned:
                print(f"  islands: {len(assigned)} reached a state across water")
            else:
                print(f"  stuck with {len(missing)} unreachable: {sorted(missing)[:10]}")
                break
        owner.update(assigned)
        missing -= set(assigned)
        rounds += 1
        print(f"  pass {rounds}: assigned {len(assigned)}, {len(missing)} left")

    final = collections.defaultdict(set)
    for p, s in owner.items():
        final[s].add(p)

    # ---- invariants ----
    errs = []
    if set(owner) != land:
        errs.append(f"coverage: {len(land - set(owner))} land provinces unassigned, "
                    f"{len(set(owner) - land)} non-land assigned")
    # A state with no provinces is not a state. These come from the 743-800
    # range, where a third layout's entries were fully absorbed by their
    # neighbours; they are dropped rather than emitted as empty shells.
    empty = sorted(s for s in states if not final.get(s))
    if empty:
        print(f"dropped {len(empty)} states left with no territory: {empty}")
    counted = sum(len(v) for v in final.values())
    if counted != len(land):
        errs.append(f"province count {counted} != land {len(land)}")
    for e in errs:
        print("  FAIL:", e)

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("id\tkey\tname\tcategory\tvanilla_owner\tprovinces\n")
        for sid in sorted(final):
            s = states[sid]
            disp = names.get(s["name"], "")
            fh.write(f"{sid}\t{s['name']}\t{disp}\t{s['category']}\t{s['vanilla_owner']}\t"
                     f"{' '.join(str(p) for p in sorted(final[sid]))}\n")

    sizes = sorted(len(v) for v in final.values())
    print(f"\nwrote {a.out}")
    print(f"  {len(final)} states covering {counted} land provinces, no gaps, no overlaps"
          if not errs else "  WROTE WITH ERRORS, see above")
    print(f"  provinces per state: min {sizes[0]}  median {sizes[len(sizes)//2]}  max {sizes[-1]}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
