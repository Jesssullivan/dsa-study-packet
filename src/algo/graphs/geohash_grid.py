"""Geohash encoding, decoding, and neighbor lookup.

Problem:
    Encode a (latitude, longitude) pair into a geohash string of a
    given precision. Decode a geohash back to a bounding box. Find
    the eight surrounding geohash cells.

Approach:
    Interleave bits of longitude and latitude ranges, then encode
    every 5 bits as a base-32 character. Decoding reverses the
    process. Neighbors are found by decoding to center, nudging
    into the adjacent cell, and re-encoding.

When to use:
    Spatial indexing for proximity queries — "find nearby points",
    "group by geographic region". Prefix-matching on geohash strings
    gives fast bounding-box lookups. Aviation: nearby airport/NAVAID
    search, sector boundary queries. See also: kd_tree for exact NN.

Complexity:
    Encode/Decode: O(precision)
    Neighbors:     O(precision) per neighbor
"""

_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_DECODE_MAP: dict[str, int] = {c: i for i, c in enumerate(_BASE32)}


def encode(lat: float, lng: float, precision: int = 12) -> str:
    """Encode latitude/longitude into a geohash string.

    >>> encode(42.6, -5.6, 5)
    'ezs42'
    """
    lat_range = (-90.0, 90.0)
    lng_range = (-180.0, 180.0)
    is_lng = True
    bits = 0
    char_index = 0
    result: list[str] = []

    while len(result) < precision:
        if is_lng:
            mid = (lng_range[0] + lng_range[1]) / 2
            if lng >= mid:
                char_index = (char_index << 1) | 1
                lng_range = (mid, lng_range[1])
            else:
                char_index = char_index << 1
                lng_range = (lng_range[0], mid)
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                char_index = (char_index << 1) | 1
                lat_range = (mid, lat_range[1])
            else:
                char_index = char_index << 1
                lat_range = (lat_range[0], mid)

        is_lng = not is_lng
        bits += 1

        if bits == 5:
            result.append(_BASE32[char_index])
            bits = 0
            char_index = 0

    return "".join(result)


def decode(geohash: str) -> tuple[tuple[float, float], tuple[float, float]]:
    """Decode a geohash into a bounding box.

    Returns ((lat_min, lat_max), (lng_min, lng_max)).

    >>> lat_range, lng_range = decode("ezs42")
    >>> round(lat_range[0], 1), round(lng_range[0], 1)
    (42.6, -5.6)
    """
    lat_range = [-90.0, 90.0]
    lng_range = [-180.0, 180.0]
    is_lng = True

    for ch in geohash:
        cd = _DECODE_MAP[ch]
        for mask in (16, 8, 4, 2, 1):
            if is_lng:
                mid = (lng_range[0] + lng_range[1]) / 2
                if cd & mask:
                    lng_range[0] = mid
                else:
                    lng_range[1] = mid
            else:
                mid = (lat_range[0] + lat_range[1]) / 2
                if cd & mask:
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid
            is_lng = not is_lng

    return (lat_range[0], lat_range[1]), (lng_range[0], lng_range[1])


def decode_center(geohash: str) -> tuple[float, float]:
    """Decode a geohash to its center (lat, lng).

    >>> lat, lng = decode_center("ezs42")
    >>> round(lat, 1), round(lng, 1)
    (42.6, -5.6)
    """
    (lat_min, lat_max), (lng_min, lng_max) = decode(geohash)
    return (lat_min + lat_max) / 2, (lng_min + lng_max) / 2


def neighbor(geohash: str, direction: str) -> str:
    """Return the geohash of the neighbor in *direction*.

    *direction* is one of 'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'.

    >>> neighbor("ezs42", "n")
    'ezs48'
    """
    if not geohash:
        msg = "Cannot compute neighbor of empty geohash"
        raise ValueError(msg)

    precision = len(geohash)
    (lat_min, lat_max), (lng_min, lng_max) = decode(geohash)
    lat_delta = lat_max - lat_min
    lng_delta = lng_max - lng_min
    center_lat = (lat_min + lat_max) / 2
    center_lng = (lng_min + lng_max) / 2

    dlat = 0.0
    dlng = 0.0
    for ch in direction:
        if ch == "n":
            dlat += lat_delta
        elif ch == "s":
            dlat -= lat_delta
        elif ch == "e":
            dlng += lng_delta
        elif ch == "w":
            dlng -= lng_delta

    new_lat = center_lat + dlat
    new_lng = center_lng + dlng

    # Clamp latitude
    new_lat = max(-89.999999, min(89.999999, new_lat))
    # Wrap longitude
    if new_lng > 180.0:
        new_lng -= 360.0
    elif new_lng < -180.0:
        new_lng += 360.0

    return encode(new_lat, new_lng, precision)


def neighbors(geohash: str) -> dict[str, str]:
    """Return all eight neighbors of a geohash cell.

    >>> sorted(neighbors("ezs42").keys())
    ['e', 'n', 'ne', 'nw', 's', 'se', 'sw', 'w']
    """
    return {
        d: neighbor(geohash, d)
        for d in ("n", "s", "e", "w", "ne", "nw", "se", "sw")
    }
