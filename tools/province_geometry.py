#!/usr/bin/env python3
"""
province_geometry.py -- province centroids and bounding boxes from provinces.bmp.

Splitting a vanilla state along an 1886 border means knowing where its provinces
physically are, and Hearts of Iron IV gives provinces no names or coordinates --
only a colour in a bitmap. This recovers position.

Accumulating 11.5 million pixels one at a time would be slow in pure Python, so
this walks runs instead. Within a scanline every pixel between two colour
boundaries belongs to the same province, and a typical row crosses only a few
dozen provinces, so the work per row is proportional to the number of provinces
it touches rather than to its width. Boundary detection is the XOR-and-translate
trick from province_adjacency.
"""

import struct
import sys

from province_adjacency import NONZERO, boundaries, load_definition


def extract(bmp_path, rgb2id):
    with open(bmp_path, "rb") as fh:
        blob = fh.read()
    off = struct.unpack("<I", blob[10:14])[0]
    w, h, _, bpp, comp = struct.unpack("<iiHHI", blob[18:34])
    if bpp != 24 or comp != 0:
        sys.exit(f"expected uncompressed 24-bit, got {bpp}-bit compression={comp}")
    h = abs(h)
    stride = (w * 3 + 3) // 4 * 4
    # BMP rows are stored bottom-up, so row 0 of the file is the last map row.
    acc = {}  # pid -> [sum_x, sum_y, n, minx, maxx, miny, maxy]
    for fy in range(h):
        y = h - 1 - fy
        row = blob[off + fy * stride: off + fy * stride + w * 3]
        cuts = [0]
        cuts.extend(i // 3 + 1 for i in boundaries(row[:-3], row[3:]))
        cuts.append(w)
        for k in range(len(cuts) - 1):
            x0, x1 = cuts[k], cuts[k + 1]
            if x1 <= x0:
                continue
            pid = rgb2id.get(row[x0 * 3:x0 * 3 + 3])
            if pid is None:
                continue
            n = x1 - x0
            sx = n * (x0 + x1 - 1) / 2.0
            a = acc.get(pid)
            if a is None:
                acc[pid] = [sx, n * y, n, x0, x1 - 1, y, y]
            else:
                a[0] += sx
                a[1] += n * y
                a[2] += n
                if x0 < a[3]: a[3] = x0
                if x1 - 1 > a[4]: a[4] = x1 - 1
                if y < a[5]: a[5] = y
                if y > a[6]: a[6] = y
    out = {}
    for pid, (sx, sy, n, x0, x1, y0, y1) in acc.items():
        out[pid] = dict(x=sx / n, y=sy / n, pixels=n, minx=x0, maxx=x1, miny=y0, maxy=y1)
    return out, (w, h)


if __name__ == "__main__":
    rgb2id, kind = load_definition(sys.argv[1])
    cent, (w, h) = extract(sys.argv[2], rgb2id)
    print(f"map {w}x{h}   provinces located: {len(cent)} of {len(rgb2id)}")
    tot = sum(c["pixels"] for c in cent.values())
    print(f"pixels accounted for: {tot:,} of {w*h:,}  ({100*tot/(w*h):.2f}%)")
    land = [p for p in cent if kind.get(p) == "land"]
    print(f"land provinces located: {len(land)}")
    xs = sorted(c["x"] for c in cent.values()); ys = sorted(c["y"] for c in cent.values())
    print(f"centroid x range {xs[0]:.0f}..{xs[-1]:.0f}   y range {ys[0]:.0f}..{ys[-1]:.0f}")
