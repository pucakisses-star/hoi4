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


def main(mod="MOD", definition=None):
    fails = []

    # Read the province table the mod itself ships, not a reference copy. A
    # province id only means anything relative to the map that defines it, so
    # checking the states against any other table proves nothing about what the
    # game will see.
    if definition is None:
        definition = os.path.join(mod, "map", "definition.csv")
    land, known = set(), set()
    if os.path.exists(definition):
        for line in open(definition, encoding="utf-8", errors="replace"):
            f = line.strip().split(";")
            if len(f) >= 5 and f[0].isdigit():
                known.add(int(f[0]))
                if f[4] == "land":
                    land.add(int(f[0]))
    land.discard(0)
    known.discard(0)

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
    wet = (set(prov_owner) & known) - land
    if wet:
        fails.append(f"{len(wet)} sea or lake provinces are inside a state")
    ghost = sorted(set(prov_owner) - known)
    if ghost:
        fails.append(f"{len(ghost)} provinces named by states are not in "
                     f"{definition}: {ghost[:8]}")

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

    # ---- the map itself ----
    # This mod's states were measured off a map that has 678 land provinces
    # vanilla does not: someone had subdivided colonial Africa, South America,
    # Persia and the Balkans. 199 states name at least one of them. Ship the
    # states without that map and those ids refer to nothing, which is what the
    # game means by "errors in the map definition".
    md = os.path.join(mod, "map")
    for need in ("definition.csv", "provinces.bmp"):
        if not os.path.exists(os.path.join(md, need)):
            fails.append(f"map/{need} is missing; the states name provinces that "
                         f"only exist in the map this mod was built from")

    srd = os.path.join(md, "strategicregions")
    if os.path.isdir(srd):
        in_region = collections.Counter()
        for fn in sorted(os.listdir(srd)):
            if not fn.endswith(".txt"):
                continue
            fp = os.path.join(srd, fn)
            if os.path.getsize(fp) == 0:
                fails.append(f"strategicregions/{fn} is empty; a file with a "
                             f"vanilla filename replaces vanilla's, so an empty "
                             f"one deletes that region and strands its provinces")
                continue
            t2 = open(fp, encoding="utf-8", errors="replace").read()
            if t2.count("{") != t2.count("}"):
                fails.append(f"strategicregions/{fn}: unbalanced braces")
            for blk in re.findall(r"provinces\s*=\s*\{([^}]*)\}", t2, re.S):
                for x in blk.split():
                    if x.isdigit():
                        in_region[int(x)] += 1
        twice = [p for p, n in in_region.items() if n > 1]
        if twice:
            fails.append(f"{len(twice)} provinces are in more than one strategic "
                         f"region: {twice[:8]}")
        stray = sorted(set(in_region) - known)
        if stray:
            fails.append(f"{len(stray)} provinces in strategic regions are not in "
                         f"definition.csv: {stray[:8]}")

    # ---- map files keyed by state id ----
    # buildings.txt, airports.txt and rocketsites.txt are keyed by state, so they
    # rot exactly the way the supply areas did the moment the state layout moves.
    QUOTA = {"arms_factory": 6, "industrial_complex": 6, "anti_air_building": 3,
             "air_base": 1, "radar_station": 1, "nuclear_reactor": 1,
             "rocket_site": 1}
    for name in ("airports.txt", "rocketsites.txt"):
        fp = os.path.join(md, name)
        if not os.path.exists(fp):
            continue
        kv = {}
        for line in open(fp, encoding="utf-8", errors="replace"):
            m = re.match(r"\s*(\d+)\s*=\s*\{\s*(\d+)", line)
            if m:
                kv[int(m.group(1))] = int(m.group(2))
        alien = sorted(set(kv) - set(ids))
        if alien:
            fails.append(f"map/{name}: {len(alien)} entries name states the mod "
                         f"does not define: {alien[:8]}")
        elsewhere = sorted(s2 for s2, p in kv.items()
                           if s2 in state_of and p not in state_of[s2])
        if elsewhere:
            fails.append(f"map/{name}: {len(elsewhere)} states are given a province "
                         f"they do not own: {elsewhere[:8]}")
        gap = sorted(set(ids) - set(kv))
        if gap:
            fails.append(f"map/{name}: {len(gap)} states have no entry: {gap[:8]}")

    bp = os.path.join(md, "buildings.txt")
    if os.path.exists(bp):
        per = collections.defaultdict(collections.Counter)
        rows = []
        orphan = 0
        for line in open(bp, encoding="utf-8", errors="replace"):
            f = line.rstrip("\n").split(";")
            if len(f) < 7 or not f[0].isdigit():
                continue
            sid = int(f[0])
            rows.append(f)
            if sid not in ids:
                orphan += 1
            per[f[1]][sid] += 1
        if orphan:
            fails.append(f"map/buildings.txt: {orphan} rows are keyed to states "
                         f"the mod does not define")
        for kind, want in sorted(QUOTA.items()):
            off = sorted(s2 for s2 in ids if per[kind].get(s2, 0) != want)
            if off:
                fails.append(f"map/buildings.txt: {len(off)} states do not have "
                             f"exactly {want} {kind}: {off[:8]}")
        bunkers = per["bunker"]
        if sum(bunkers.values()) != len(land):
            fails.append(f"map/buildings.txt: {sum(bunkers.values())} bunkers for "
                         f"{len(land)} land provinces; the format wants one each")
        # A building's position has to fall inside the state it is keyed to.
        bmp = os.path.join(md, "provinces.bmp")
        if rows and os.path.exists(bmp) and os.path.exists(definition):
            try:
                from emit_mapfiles import Provinces
            except ImportError:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from emit_mapfiles import Provinces
            pr = Provinces(bmp, definition)
            outside = 0
            for f in rows:
                p = pr.at(float(f[2]), float(f[4]))
                if prov_owner.get(p, [None])[0] != int(f[0]):
                    outside += 1
            if outside:
                fails.append(f"map/buildings.txt: {outside} rows sit at a position "
                             f"that is not inside the state they are keyed to")

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
