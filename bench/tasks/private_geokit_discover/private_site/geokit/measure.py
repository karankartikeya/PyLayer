from __future__ import annotations

import math
from collections.abc import Iterable

from geokit.points import GeoPoint

EARTH_RADIUS_KM = 6371.0088  # IUGG mean radius


def haversine_km(a: GeoPoint, b: GeoPoint) -> float:
    """Great-circle distance between two points in kilometres."""
    p1, p2 = math.radians(a.lat), math.radians(b.lat)
    dp, dl = p2 - p1, math.radians(b.lon - a.lon)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(h))


class Route:
    """An ordered sequence of GeoPoints."""

    def __init__(self, points: Iterable[GeoPoint] = ()) -> None:
        self._points: list[GeoPoint] = list(points)

    def add(self, point: GeoPoint) -> Route:
        self._points.append(point)
        return self

    @property
    def points(self) -> tuple[GeoPoint, ...]:
        return tuple(self._points)

    @property
    def length_km(self) -> float:
        return sum(haversine_km(a, b) for a, b in zip(self._points, self._points[1:]))

    def bbox(self) -> tuple[GeoPoint, GeoPoint]:
        """(south-west corner, north-east corner). Raises ValueError for an empty route."""
        if not self._points:
            raise ValueError("empty route")
        lats = [p.lat for p in self._points]
        lons = [p.lon for p in self._points]
        return GeoPoint(min(lats), min(lons)), GeoPoint(max(lats), max(lons))
