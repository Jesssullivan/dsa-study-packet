---
title: Geohash Grid
---

# Geohash Grid

## Problem

Encode a (latitude, longitude) pair into a geohash string of a
given precision. Decode a geohash back to a bounding box. Find
the eight surrounding geohash cells.

## Approach

Interleave bits of longitude and latitude ranges, then encode
every 5 bits as a base-32 character. Decoding reverses the
process. Neighbors are found by decoding to center, nudging
into the adjacent cell, and re-encoding.

## When to Use

Spatial indexing for proximity queries — "find nearby points",
"group by geographic region". Prefix-matching on geohash strings
gives fast bounding-box lookups. Aviation: nearby airport/NAVAID
search, sector boundary queries. See also: kd_tree for exact NN.

## Implementation

=== "Solution"

    ::: algo.graphs.geohash_grid
        options:
          show_source: true

=== "Tests"

    ```python title="tests/graphs/test_geohash_grid.py"
    --8<-- "tests/graphs/test_geohash_grid.py"
    ```

=== "Challenge"

    !!! question "Implement it yourself"

        **Run:** `just challenge graphs geohash_grid`

        Then implement the functions to make all tests pass.
        Use `just study graphs` for watch mode.

    ??? success "Reveal Solution"

        ::: algo.graphs.geohash_grid
            options:
              show_source: true
