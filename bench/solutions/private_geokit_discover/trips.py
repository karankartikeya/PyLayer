from geokit import GeoPoint, Route


def _route(coords: list[tuple[float, float]]) -> Route:
    return Route(GeoPoint(lat, lon) for lat, lon in coords)


def trip_length_km(coords: list[tuple[float, float]]) -> float:
    return _route(coords).length_km


def trip_bounds(coords: list[tuple[float, float]]) -> dict:
    sw, ne = _route(coords).bbox()
    return {"south": sw.lat, "west": sw.lon, "north": ne.lat, "east": ne.lon}
