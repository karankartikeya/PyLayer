Our internal `geokit` package is installed in the project venv. Using it (please don't reimplement the geo math yourself), create `trips.py` with:

- `trip_length_km(coords: list[tuple[float, float]]) -> float`: total length of a trip through the given `(lat, lon)` points, in order.
- `trip_bounds(coords: list[tuple[float, float]]) -> dict`: `{"south": ..., "west": ..., "north": ..., "east": ...}` for the trip.

Invalid coordinates should raise `ValueError`.
