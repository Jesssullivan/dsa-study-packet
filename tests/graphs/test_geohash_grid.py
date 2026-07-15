"""Tests for geohash encoding, decoding, and neighbors."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.geohash_grid import decode, decode_center, encode, neighbor, neighbors


class TestEncode:
    def test_known_hash(self) -> None:
        assert encode(42.6, -5.6, 5) == "ezs42"

    def test_origin(self) -> None:
        h = encode(0.0, 0.0, 5)
        assert len(h) == 5

    def test_precision(self) -> None:
        assert len(encode(51.5, -0.1, 8)) == 8

    def test_negative_coords(self) -> None:
        h = encode(-33.8688, 151.2093, 6)
        assert len(h) == 6


class TestDecode:
    def test_roundtrip(self) -> None:
        lat, lng = 42.6, -5.6
        h = encode(lat, lng, 8)
        (lat_min, lat_max), (lng_min, lng_max) = decode(h)
        assert lat_min <= lat <= lat_max
        assert lng_min <= lng <= lng_max

    def test_center_roundtrip(self) -> None:
        lat, lng = 37.7749, -122.4194
        h = encode(lat, lng, 9)
        clat, clng = decode_center(h)
        assert abs(clat - lat) < 0.001
        assert abs(clng - lng) < 0.001


class TestNeighbor:
    def test_north(self) -> None:
        n = neighbor("ezs42", "n")
        assert n == "ezs48"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError):
            neighbor("", "n")

    def test_all_eight_neighbors(self) -> None:
        nbrs = neighbors("ezs42")
        assert len(nbrs) == 8
        assert all(len(v) == 5 for v in nbrs.values())

    def test_neighbor_adjacency(self) -> None:
        """North neighbor's south neighbor should be the original."""
        original = "ezs42"
        north = neighbor(original, "n")
        back = neighbor(north, "s")
        assert back == original


class TestGeohashProperties:
    @given(
        lat=st.floats(min_value=-89.0, max_value=89.0, allow_nan=False),
        lng=st.floats(min_value=-179.0, max_value=179.0, allow_nan=False),
        precision=st.integers(min_value=1, max_value=10),
    )
    def test_encode_decode_roundtrip_contains_point(
        self, lat: float, lng: float, precision: int
    ) -> None:
        h = encode(lat, lng, precision)
        (lat_min, lat_max), (lng_min, lng_max) = decode(h)
        assert lat_min <= lat <= lat_max
        assert lng_min <= lng <= lng_max

    @given(
        lat=st.floats(min_value=-80.0, max_value=80.0, allow_nan=False),
        lng=st.floats(min_value=-170.0, max_value=170.0, allow_nan=False),
        direction=st.sampled_from(("n", "s", "e", "w")),
    )
    def test_cardinal_neighbor_is_reversible(
        self, lat: float, lng: float, direction: str
    ) -> None:
        """Walking n/s/e/w and back on any cell returns to the same geohash."""
        opposite = {"n": "s", "s": "n", "e": "w", "w": "e"}
        h = encode(lat, lng, 6)
        moved = neighbor(h, direction)
        back = neighbor(moved, opposite[direction])
        assert back == h
