#!/usr/bin/env python3
"""
province_adjacency.py -- derive which provinces touch which, straight from
provinces.bmp, with no image library.

provinces.bmp is an uncompressed 24-bit bitmap in which every province is a
solid block of one RGB value, and definition.csv maps that RGB to a province
id. Two provinces are neighbours if any of their pixels are edge-adjacent.

Scanning 11.5 million pixels in a Python loop is slow, so boundaries are found
without one: XOR a row against itself shifted by one pixel, collapse the result
to a 0/1 mask with bytes.translate (C speed), then walk the mask with
bytes.find, which only iterates once per boundary rather than once per pixel.
The same trick finds vertical boundaries between consecutive rows.
"""

import collections
import struct
import sys

NONZERO = bytes([0] + [1] * 255)  # 0 stays 0, everything else becomes 1


def load_definition(path):
    rgb2id, kind = {}, {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            f = line.strip().split(";")
            if len(f) >= 5 and f[0].isdigit():
                pid = int(f[0])
                rgb2id[bytes((int(f[3]), int(f[2]), int(f[1])))] = pid  # BMP is BGR
                kind[pid] = f[4].strip().lower()
    return rgb2id, kind


def boundaries(a, b):
    """Byte offsets where 3-byte pixels in a and b differ. a and b same length."""
    if a == b:
        return
    x = (int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).to_bytes(len(a), "big")
    mask = x.translate(NONZERO)
    pos = mask.find(b"\x01")
    while pos != -1:
        yield pos - pos % 3
        # skip to the end of this pixel; boundaries are sparse so this is cheap
        pos = mask.find(b"\x01", pos - pos % 3 + 3)


def adjacency(bmp_path, rgb2id):
    with open(bmp_path, "rb") as fh:
        blob = fh.read()
    off = struct.unpack("<I", blob[10:14])[0]
    w, h, _, bpp, comp = struct.unpack("<iiHHI", blob[18:34])
    if bpp != 24 or comp != 0:
        sys.exit(f"expected uncompressed 24-bit, got {bpp}-bit compression={comp}")
    stride = (w * 3 + 3) // 4 * 4
    rows = [blob[off + y * stride: off + y * stride + w * 3] for y in range(abs(h))]

    adj = collections.defaultdict(set)
    unknown = collections.Counter()

    def link(p1, p2):
        a, b_ = rgb2id.get(p1), rgb2id.get(p2)
        if a is None:
            unknown[p1] += 1
        if b_ is None:
            unknown[p2] += 1
        if a is not None and b_ is not None and a != b_:
            adj[a].add(b_)
            adj[b_].add(a)

    for row in rows:  # horizontal
        for i in boundaries(row[:-3], row[3:]):
            link(row[i:i + 3], row[i + 3:i + 6])
    for y in range(len(rows) - 1):  # vertical
        r1, r2 = rows[y], rows[y + 1]
        for i in boundaries(r1, r2):
            link(r1[i:i + 3], r2[i:i + 3])
    return adj, unknown, (w, abs(h))


if __name__ == "__main__":
    defn, bmp = sys.argv[1], sys.argv[2]
    rgb2id, kind = load_definition(defn)
    adj, unknown, dims = adjacency(bmp, rgb2id)
    print(f"map {dims[0]}x{dims[1]}   provinces in definition.csv: {len(rgb2id)}")
    print(f"provinces with at least one neighbour: {len(adj)}")
    print(f"total adjacency pairs: {sum(len(v) for v in adj.values()) // 2}")
    print(f"colours in the bitmap not in definition.csv: {len(unknown)}")
    isolated = [p for p in kind if p not in adj and kind[p] == "land"]
    print(f"land provinces with no neighbour at all: {len(isolated)} {isolated[:8]}")
    deg = sorted(len(v) for v in adj.values())
    print(f"neighbours per province: min {deg[0]}  median {deg[len(deg)//2]}  max {deg[-1]}")
