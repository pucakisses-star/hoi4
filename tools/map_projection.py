#!/usr/bin/env python3
"""
map_projection.py -- turn provinces.bmp pixel coordinates into real latitude and
longitude, so 1886 borders can be drawn against the actual world.

Hearts of Iron IV gives provinces no coordinates, and its map is not a clean
projection -- longitude runs close to linear across the whole width, but
latitude is stretched near the poles and compressed in the far south, so no
single global formula fits well. Rather than fight that, this fits a local
affine transform per region from anchor states whose real position is known,
and reports the residual so the fit can be trusted or rejected on evidence.

An affine fit (lat and lon each a linear function of x and y) absorbs the
rotation and shear in the projection, which a plain axis-aligned scale cannot.
"""

import json
import math
import sys

# state display name -> (latitude, longitude) of that region's real centre
ANCHORS_EUROPE = {
    "Lisbon":               (38.7, -9.1),
    "Madrid Area":          (40.4, -3.7),
    "Porto":                (41.1, -8.6),
    "Catalonia":            (41.6, 1.6),
    "Ile de France":        (48.9, 2.3),
    "Greater London Area":  (51.5, -0.1),
    "Lothian":              (55.9, -3.2),
    "Leinster":             (53.3, -6.3),
    "Noord-Holland":        (52.4, 4.9),
    "Brabant":              (50.8, 4.4),
    "Brandenburg":          (52.5, 13.4),
    "Saxony":               (51.0, 13.7),
    "Upper Bavaria":        (48.1, 11.6),
    "Wurttemberg":          (48.8, 9.2),
    "Rhineland":            (50.9, 7.0),
    "Bohemia":              (50.1, 14.4),
    "Lower Austria":        (48.2, 16.4),
    "Sjaelland":            (55.7, 12.6),
    "Svealand":             (59.3, 18.1),
    "Uusimaa":              (60.2, 24.9),
    "Sankt Petersburg":     (59.9, 30.3),
    "Moscow Area":          (55.8, 37.6),
    "East Prussia":         (54.7, 20.5),
    "Mazowsze":             (52.2, 21.0),
    "Kiev":                 (50.5, 30.5),
    "Lombardy":             (45.5, 9.2),
    "Lazio":                (41.9, 12.5),
    "Romandy":              (46.8, 7.1),
    "Sofia":                (42.7, 23.3),
    "Thrace":               (41.0, 28.0),
}


def solve3(a, b):
    """Gaussian elimination for a 3x3 system."""
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r: abs(m[r][i]))
        m[i], m[p] = m[p], m[i]
        if abs(m[i][i]) < 1e-12:
            raise ValueError("singular anchor set")
        for r in range(3):
            if r == i:
                continue
            f = m[r][i] / m[i][i]
            for c in range(i, 4):
                m[r][c] -= f * m[i][c]
    return [m[i][3] / m[i][i] for i in range(3)]


def fit(centroids, anchors):
    """Least-squares affine: value = k0*x + k1*y + k2, for lat and lon."""
    pts = [(centroids[n][0], centroids[n][1], v) for n, v in anchors.items() if n in centroids]
    if len(pts) < 3:
        raise ValueError(f"need at least 3 anchors present, found {len(pts)}")

    def solve_for(idx):
        A = [[0.0] * 3 for _ in range(3)]
        B = [0.0] * 3
        for x, y, v in pts:
            basis = (x, y, 1.0)
            for i in range(3):
                for j in range(3):
                    A[i][j] += basis[i] * basis[j]
                B[i] += basis[i] * v[idx]
        return solve3(A, B)

    return solve_for(0), solve_for(1), len(pts)


class Projection:
    def __init__(self, klat, klon):
        self.klat, self.klon = klat, klon

    def __call__(self, x, y):
        a, b, c = self.klat
        d, e, f = self.klon
        return a * x + b * y + c, d * x + e * y + f


def residuals(proj, centroids, anchors):
    out = []
    for n, (lat, lon) in anchors.items():
        if n not in centroids:
            continue
        plat, plon = proj(*centroids[n])
        dlat = (plat - lat) * 111.0
        dlon = (plon - lon) * 111.0 * math.cos(math.radians(lat))
        out.append((math.hypot(dlat, dlon), n, plat, plon, lat, lon))
    out.sort(reverse=True)
    return out


if __name__ == "__main__":
    centroids = json.load(open(sys.argv[1]))
    klat, klon, n = fit(centroids, ANCHORS_EUROPE)
    proj = Projection(klat, klon)
    res = residuals(proj, centroids, ANCHORS_EUROPE)
    errs = sorted(r[0] for r in res)
    print(f"affine fit on {n} European anchors")
    print(f"  lat = {klat[0]:+.6f}*x {klat[1]:+.6f}*y {klat[2]:+.3f}")
    print(f"  lon = {klon[0]:+.6f}*x {klon[1]:+.6f}*y {klon[2]:+.3f}")
    print(f"\nresidual km:  median {errs[len(errs)//2]:.0f}   "
          f"90th {errs[int(len(errs)*0.9)]:.0f}   worst {errs[-1]:.0f}")
    print("\nworst six:")
    for e, nm, plat, plon, alat, alon in res[:6]:
        print(f"  {nm:<22} {e:6.0f} km   fit {plat:5.1f},{plon:6.1f}   real {alat:5.1f},{alon:6.1f}")
