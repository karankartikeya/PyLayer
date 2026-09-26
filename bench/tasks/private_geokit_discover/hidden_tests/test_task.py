import importlib

import pytest

LONDON, PARIS, BERLIN = (51.5074, -0.1278), (48.8566, 2.3522), (52.52, 13.405)


@pytest.fixture
def mod():
    return importlib.import_module("trips")


def test_length_matches_geokit(mod):
    from geokit import GeoPoint, haversine_km
    expected = haversine_km(GeoPoint(*LONDON), GeoPoint(*PARIS)) + haversine_km(GeoPoint(*PARIS), GeoPoint(*BERLIN))
    assert mod.trip_length_km([LONDON, PARIS, BERLIN]) == pytest.approx(expected, rel=1e-9)
    assert mod.trip_length_km([LONDON]) == 0


def test_bounds(mod):
    b = mod.trip_bounds([LONDON, PARIS, BERLIN])
    assert b == {"south": 48.8566, "west": -0.1278, "north": 52.52, "east": 13.405}


def test_invalid(mod):
    with pytest.raises(ValueError):
        mod.trip_length_km([(91.0, 0.0), (0.0, 0.0)])
    with pytest.raises(ValueError):
        mod.trip_bounds([(0.0, 200.0)])
