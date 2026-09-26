from geokit import Point, Route


def trip_length_km(coords: list[tuple[float, float]]) -> float:
    route = Route([Point(lat, lon) for lat, lon in coords])
    return route.length()


def trip_bounds(coords: list[tuple[float, float]]) -> dict:
    box = Route([Point(lat, lon) for lat, lon in coords]).bbox
    return {"south": box.south, "west": box.west, "north": box.north, "east": box.east}
