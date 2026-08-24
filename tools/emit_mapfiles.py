#!/usr/bin/env python3
"""Rebuild the state-keyed map files for this mod's state layout.

map/buildings.txt, map/airports.txt and map/rocketsites.txt are keyed by state
id.  The copies that ship with the map were generated for a 1,327-state layout;
this mod defines 857 states, so most of those keys are either stale or point at
a position that now lies in a different state.  That is the same class of defect
as the supply areas: a map file naming states that do not exist.

Nothing here is invented.  Every position is either taken verbatim from the
reference file -- re-keyed to whichever state actually contains it, determined
by reading the pixel out of provinces.bmp -- or, where a state would otherwise
be short of the per-state quota the format requires, placed on a real pixel of
one of that state's own provinces.
"""
import collections
import os
import re
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "MOD", "map")
DATA = os.path.join(ROOT, "tools", "data")
STATES = os.path.join(ROOT, "MOD", "history", "states")

# How many of each building the format wants per state, per land province and
# per coastal province.  Measured from the reference file, where all 1,327
# states agree exactly.
PER_STATE = {
    "arms_factory": 6,
    "industrial_complex": 6,
    "anti_air_building": 3,
    "air_base": 1,
    "radar_station": 1,
    "nuclear_reactor": 1,
    "rocket_site": 1,
}
PER_LAND_PROVINCE = ["bunker"]
PER_COASTAL_PROVINCE = ["coastal_bunker", "naval_base"]
PER_COASTAL_STATE = ["dockyard"]
ORDER = (list(PER_STATE) + PER_LAND_PROVINCE
         + PER_COASTAL_PROVINCE + PER_COASTAL_STATE)


class Provinces:
    """The province bitmap, indexed so a map position resolves to a province."""

    def __init__(self, bmp_path, definition_path):
        raw = open(bmp_path, "rb").read()
        off = struct.unpack_from("<I", raw, 10)[0]
        w, h = struct.unpack_from("<ii", raw, 18)
        bpp = struct.unpack_from("<H", raw, 28)[0]
        if bpp != 24 or struct.unpack_from("<I", raw, 30)[0] != 0:
            sys.exit(f"{bmp_path}: expected an uncompressed 24-bit bitmap")
        self.raw, self.off, self.w, self.h = raw, off, w, abs(h)
        self.stride = (w * 3 + 3) // 4 * 4

        self.colour = {}          # id -> (r, g, b)
        self.kind = {}            # id -> land / sea / lake
        self.coastal = set()
        by_colour = {}
        for line in open(definition_path, encoding="utf-8-sig"):
            f = line.rstrip("\n").split(";")
            if len(f) < 8 or not f[0].isdigit():
                continue
            i = int(f[0])
            rgb = (int(f[1]), int(f[2]), int(f[3]))
            self.colour[i], self.kind[i] = rgb, f[4]
            if f[5].strip().lower() == "true":
                self.coastal.add(i)
            by_colour[rgb] = i
        self.by_colour = by_colour

    def at(self, x, z):
        """Province at a map position.  z is measured from the bottom edge."""
        c, r = int(x), int(z)
        if not (0 <= c < self.w and 0 <= r < self.h):
            return None
        o = self.off + r * self.stride + c * 3
        b, g, r_ = self.raw[o], self.raw[o + 1], self.raw[o + 2]
        return self.by_colour.get((r_, g, b))

    def sample_pixels(self, wanted, step):
        """One real pixel per wanted province, as {id: (x, z)}."""
        found = {}
        for row in range(0, self.h, step):
            base = self.off + row * self.stride
            for col in range(0, self.w, step):
                o = base + col * 3
                i = self.by_colour.get(
                    (self.raw[o + 2], self.raw[o + 1], self.raw[o]))
                if i in wanted and i not in found:
                    found[i] = (col + 0.5, row + 0.5)
                    if len(found) == len(wanted):
                        return found
        return found


def load_states():
    states = {}
    for name in sorted(os.listdir(STATES)):
        if not name.endswith(".txt"):
            continue
        text = open(os.path.join(STATES, name),
                    encoding="utf-8-sig", errors="replace").read()
        sid = re.search(r"\bid\s*=\s*(\d+)", text)
        prov = re.search(r"provinces\s*=\s*\{([^}]*)\}", text, re.S)
        if not sid or not prov:
            sys.exit(f"{name}: no id or no province list")
        states[int(sid.group(1))] = [int(x) for x in prov.group(1).split()]
    return states


def load_reference(name):
    rows = []
    for line in open(os.path.join(DATA, name), encoding="utf-8-sig"):
        f = line.rstrip("\n").rstrip("\r").split(";")
        if len(f) >= 7 and f[0].isdigit():
            rows.append(f)
    return rows


def main():
    pr = Provinces(os.path.join(MAP, "provinces.bmp"),
                   os.path.join(MAP, "definition.csv"))
    states = load_states()
    owner = {}
    for sid, provs in states.items():
        for p in provs:
            owner[p] = sid
    print(f"states {len(states)}, provinces {len(owner)}, "
          f"bitmap {pr.w}x{pr.h}")

    # Re-key every reference row by the province its position actually falls in.
    rows = load_reference("buildings_reference.txt")
    by_state = collections.defaultdict(lambda: collections.defaultdict(list))
    at_province = collections.defaultdict(dict)
    orphan = 0
    for f in rows:
        p = pr.at(float(f[2]), float(f[4]))
        sid = owner.get(p)
        if sid is None:
            orphan += 1
            continue
        by_state[sid][f[1]].append(f)
        at_province[f[1]].setdefault(p, f)
    print(f"reference rows {len(rows)}, re-keyed {len(rows) - orphan}, "
          f"outside every state {orphan}")

    # Which states are short of the per-state quota, and of what?
    short = collections.Counter()
    need_pixel = set()
    for sid, provs in states.items():
        land = [p for p in provs if pr.kind.get(p) == "land"]
        for kind, want in PER_STATE.items():
            have = len(by_state[sid][kind])
            if have < want:
                short[kind] += want - have
                need_pixel.update(land[:1])
        if any(p in pr.coastal for p in land) and not by_state[sid]["dockyard"]:
            short["dockyard"] += 1
            need_pixel.update([p for p in land if p in pr.coastal][:1])
    for kind in PER_LAND_PROVINCE:
        for p in owner:
            if pr.kind.get(p) == "land" and p not in at_province[kind]:
                short[kind] += 1
                need_pixel.add(p)
    pixel = pr.sample_pixels(need_pixel, 4) if need_pixel else {}
    missing = need_pixel - set(pixel)
    if missing:
        pixel.update(pr.sample_pixels(missing, 1))
    if short:
        print("positions to place: "
              + ", ".join(f"{k} {v}" for k, v in sorted(short.items())))
        print(f"provinces needing a representative pixel: {len(need_pixel)}, "
              f"resolved {len(pixel)}")

    def height_for(sid):
        ys = [float(f[3]) for kind in by_state[sid]
              for f in by_state[sid][kind]]
        return sorted(ys)[len(ys) // 2] if ys else 9.75

    def place(sid, kind, province, sea="0"):
        x, z = pixel[province]
        return [str(sid), kind, f"{x:.2f}", f"{height_for(sid):.2f}",
                f"{z:.2f}", "0.00", sea]

    out = []
    for sid in sorted(states):
        land = [p for p in states[sid] if pr.kind.get(p) == "land"]
        coastal = [p for p in land if p in pr.coastal]
        for kind in ORDER:
            if kind in PER_STATE:
                chosen = by_state[sid][kind][:PER_STATE[kind]]
                while len(chosen) < PER_STATE[kind]:
                    chosen.append(place(sid, kind, land[0]))
            elif kind in PER_LAND_PROVINCE:
                chosen = []
                for p in land:
                    f = at_province[kind].get(p)
                    chosen.append(f if f else place(sid, kind, p))
            elif kind in PER_COASTAL_PROVINCE:
                chosen = [at_province[kind][p] for p in coastal
                          if p in at_province[kind]]
            else:
                chosen = by_state[sid][kind][:1]
                if coastal and not chosen:
                    chosen = [place(sid, kind, coastal[0])]
            for f in chosen:
                out.append(";".join([str(sid)] + list(f[1:])))

    with open(os.path.join(MAP, "buildings.txt"), "w",
              encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"map/buildings.txt: {len(out)} rows")

    # airports and rocketsites name one province per state.  Derive them from
    # the positions just written so the three files cannot disagree.
    written = collections.defaultdict(dict)
    for line in out:
        f = line.split(";")
        written[f[1]][int(f[0])] = pr.at(float(f[2]), float(f[4]))
    for name, kind in (("airports.txt", "air_base"),
                       ("rocketsites.txt", "rocket_site")):
        lines = []
        for sid in sorted(states):
            p = written[kind].get(sid)
            if p is None or owner.get(p) != sid:
                land = [q for q in states[sid] if pr.kind.get(q) == "land"]
                p = land[0]
            lines.append(f"{sid}={{{p} }}")
        with open(os.path.join(MAP, name), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"map/{name}: {len(lines)} states")


if __name__ == "__main__":
    main()
