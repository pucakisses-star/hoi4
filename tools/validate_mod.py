#!/usr/bin/env python3
"""
validate_mod.py -- check the generated mod against the invariants that matter,
by reading the files the game will read rather than the tables they came from.

Every check here corresponds to something that actually went wrong in the
previous version of this mod, or in this one during its rebuild.
"""

import collections
import os
import re
import sys

ID = re.compile(r"\bid\s*=\s*(\d+)")
PROV = re.compile(r"provinces\s*=\s*\{([^}]*)\}", re.S)
OWNER = re.compile(r"\bowner\s*=\s*([A-Z0-9]{3})")
VP = re.compile(r"victory_points\s*=\s*\{\s*(\d+)\s+(\d+)\s*\}")
CAPITAL = re.compile(r"^capital\s*=\s*(\d+)", re.M)
OOB = re.compile(r'^oob\s*=\s*"([^"]+)"', re.M)
RULING = re.compile(r"ruling_party\s*=\s*(\w+)")
POPS = re.compile(r"set_popularities\s*=\s*\{([^}]*)\}", re.S)
LOC = re.compile(r"^\s*location\s*=\s*(\d+)", re.M)
TMPL = re.compile(r'division_template\s*=\s*\{[^{]*name\s*=\s*"([^"]+)"', re.S)
USES = re.compile(r'division_template\s*=\s*"([^"]+)"')


def main(mod="MOD", definition="tools/data/definition_reference.csv"):
    fails = []

    land = set()
    for line in open(definition, encoding="utf-8", errors="replace"):
        f = line.strip().split(";")
        if len(f) >= 5 and f[0].isdigit() and f[4] == "land":
            land.add(int(f[0]))
    land.discard(0)

    # ---- states ----
    sd = os.path.join(mod, "history", "states")
    ids = collections.Counter()
    prov_owner = collections.defaultdict(list)
    state_of = {}
    owner_states = collections.defaultdict(set)
    for fn in sorted(os.listdir(sd)):
        if not fn.endswith(".txt"):
            continue
        t = open(os.path.join(sd, fn), encoding="utf-8").read()
        if t.count("{") != t.count("}"):
            fails.append(f"states/{fn}: unbalanced braces")
        m, o = ID.search(t), OWNER.search(t)
        if not m:
            fails.append(f"states/{fn}: no id")
            continue
        sid = int(m.group(1))
        ids[sid] += 1
        ps = {int(x) for b in PROV.findall(t) for x in b.split() if x.isdigit()}
        if not ps:
            fails.append(f"states/{fn}: no provinces")
        for p in ps:
            prov_owner[p].append(sid)
        state_of[sid] = ps
        if o:
            owner_states[o.group(1)].add(sid)
        else:
            fails.append(f"states/{fn}: no owner")
        for v in VP.finditer(t):
            if int(v.group(1)) not in ps:
                fails.append(f"states/{fn}: victory point on province it does not own")
    for sid, n in ids.items():
        if n > 1:
            fails.append(f"state id {sid} defined {n} times")
    for p, v in prov_owner.items():
        if len(v) > 1:
            fails.append(f"province {p} claimed by states {v}")
    miss = land - set(prov_owner)
    if miss:
        fails.append(f"{len(miss)} land provinces belong to no state")
    wet = set(prov_owner) - land
    if wet:
        fails.append(f"{len(wet)} sea or lake provinces are inside a state")

    # ---- countries ----
    cd = os.path.join(mod, "history", "countries")
    oobs = {}
    for fn in sorted(os.listdir(cd)):
        if not fn.endswith(".txt"):
            continue
        tag = fn[:3]
        t = open(os.path.join(cd, fn), encoding="utf-8").read()
        if t.count("{") != t.count("}"):
            fails.append(f"countries/{fn}: unbalanced braces")
        c = CAPITAL.search(t)
        if not c:
            fails.append(f"countries/{fn}: no capital")
        elif int(c.group(1)) not in owner_states.get(tag, ()):
            fails.append(f"countries/{fn}: capital {c.group(1)} is not a state {tag} owns")
        r = RULING.search(t)
        pm = POPS.search(t)
        if not r:
            fails.append(f"countries/{fn}: no ruling_party")
        if pm:
            tot = sum(int(x) for x in re.findall(r"=\s*(\d+)", pm.group(1)))
            if tot != 100:
                fails.append(f"countries/{fn}: popularities sum to {tot}")
            if r and r.group(1) not in pm.group(1):
                fails.append(f"countries/{fn}: ruling party has no popularity entry")
        ob = OOB.search(t)
        if ob:
            oobs[tag] = ob.group(1)
    missing_country = sorted(set(owner_states) - {f[:3] for f in os.listdir(cd)})
    if missing_country:
        fails.append(f"countries owning states but with no country file: {missing_country}")

    # ---- orders of battle ----
    ud = os.path.join(mod, "history", "units")
    for tag, name in sorted(oobs.items()):
        p = os.path.join(ud, name + ".txt")
        if not os.path.exists(p):
            fails.append(f"countries/{tag}: oob {name!r} has no file")
            continue
        t = open(p, encoding="utf-8").read()
        if t.count("{") != t.count("}"):
            fails.append(f"units/{name}: unbalanced braces")
        owned = set()
        for sid in owner_states[tag]:
            owned |= state_of[sid]
        for m in LOC.finditer(t):
            if int(m.group(1)) not in owned:
                fails.append(f"units/{name}: division at province {m.group(1)}, "
                             f"which {tag} does not own")
        defined = set(TMPL.findall(t))
        for u in set(USES.findall(t)):
            if u not in defined:
                fails.append(f"units/{name}: uses undefined template {u!r}")

    # ---- supply areas ----
    # Every state must be in exactly one, and no area may name a state that
    # does not exist. Failing either makes the game refuse to load the map,
    # which is how this mod failed its first playable launch.
    sa = os.path.join(mod, "map", "supplyareas")
    if os.path.isdir(sa):
        in_area = collections.Counter()
        for fn in sorted(os.listdir(sa)):
            if not fn.endswith(".txt"):
                continue
            t2 = open(os.path.join(sa, fn), encoding="utf-8").read()
            if t2.count("{") != t2.count("}"):
                fails.append(f"supplyareas/{fn}: unbalanced braces")
            for blk in re.findall(r"states\s*=\s*\{([^}]*)\}", t2, re.S):
                for x in blk.split():
                    if x.isdigit():
                        in_area[int(x)] += 1
                        if int(x) not in ids:
                            fails.append(f"supplyareas/{fn}: names state {x}, "
                                         f"which the mod does not define")
        twice = [s for s, n in in_area.items() if n > 1]
        if twice:
            fails.append(f"{len(twice)} states are in more than one supply area: {twice[:8]}")
        none = sorted(set(ids) - set(in_area))
        if none:
            fails.append(f"{len(none)} states are in no supply area: {none[:8]}")
    else:
        fails.append("map/supplyareas is missing; vanilla's will be used and it "
                     "knows nothing about this mod's new states")

    # ---- filenames that shadow vanilla's ----
    # Hearts of Iron IV overrides most directories by filename. Shipping a file
    # with a base-game name silently DELETES vanilla's version of it. That is
    # how this mod crashed on its first launch: common/country_tags/00_countries.txt
    # is vanilla's own filename, so shipping it removed all ~190 base-game tags
    # and left 73 state owners -- France, Britain, the United States among them --
    # pointing at countries that no longer existed.
    SHADOW = {
        "common/country_tags/00_countries.txt":
            "deletes every vanilla country tag; use a different filename so it is additive",
        "common/country_tags/zz_dynamic_countries.txt":
            "deletes vanilla's dynamic tag pool used for civil wars and released nations",
        "common/ideologies/00_ideologies.txt":
            "deletes vanilla's ideologies; every idea and focus referencing one stops resolving",
        "common/units/00_infantry.txt":
            "deletes vanilla's infantry unit definitions",
        "common/state_category/00_state_categories.txt":
            "deletes vanilla's state categories, which every state file references",
    }
    for rel, why in SHADOW.items():
        if os.path.exists(os.path.join(mod, rel)):
            fails.append(f"{rel} shadows a vanilla filename: {why}")

    # colors.txt genuinely has no alternative name, so it must be complete
    cpath = os.path.join(mod, "common", "countries", "colors.txt")
    if os.path.exists(cpath):
        ct = open(cpath, encoding="utf-8").read()
        coloured = set(re.findall(r"^([A-Z0-9]{3})\s*=", ct, re.M))
        gap = sorted(set(owner_states) - coloured)
        if gap:
            fails.append(f"colors.txt replaces vanilla's but has no colour for "
                         f"{len(gap)} tags in use: {gap[:8]}")

    # ---- bookmarks ----
    bd = os.path.join(mod, "common", "bookmarks")
    if os.path.isdir(bd):
        have = {f[:3] for f in os.listdir(cd)}
        for fn in os.listdir(bd):
            t = open(os.path.join(bd, fn), encoding="utf-8").read()
            if t.count("{") != t.count("}"):
                fails.append(f"bookmarks/{fn}: unbalanced braces")
            for tag in re.findall(r'"([A-Z]{3})"\s*=', t):
                if tag not in have:
                    fails.append(f"bookmarks/{fn}: features {tag}, which has no country file")

    print(f"states      {len(ids)}")
    print(f"countries   {len(os.listdir(cd))}")
    print(f"oob files   {len(os.listdir(ud))}")
    print(f"provinces   {len(prov_owner)} of {len(land)} land")
    print()
    if fails:
        print(f"FAILED: {len(fails)} problems")
        for f in fails[:20]:
            print("  " + f)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
