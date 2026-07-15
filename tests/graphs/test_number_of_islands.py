"""Tests for the number of islands problem."""

from hypothesis import given
from hypothesis import strategies as st

from algo.graphs.number_of_islands import num_islands


class TestNumIslands:
    def test_single_island(self) -> None:
        grid = [
            ["1", "1", "1"],
            ["0", "1", "0"],
            ["0", "0", "0"],
        ]
        assert num_islands(grid) == 1

    def test_two_islands(self) -> None:
        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"],
        ]
        assert num_islands(grid) == 3

    def test_all_water(self) -> None:
        grid = [["0", "0"], ["0", "0"]]
        assert num_islands(grid) == 0

    def test_all_land(self) -> None:
        grid = [["1", "1"], ["1", "1"]]
        assert num_islands(grid) == 1

    def test_empty_grid(self) -> None:
        assert num_islands([]) == 0
        assert num_islands([[]]) == 0

    def test_single_cell(self) -> None:
        assert num_islands([["1"]]) == 1
        assert num_islands([["0"]]) == 0


@st.composite
def random_grids(
    draw: st.DrawFn, max_rows: int = 6, max_cols: int = 6
) -> list[list[str]]:
    rows = draw(st.integers(min_value=1, max_value=max_rows))
    cols = draw(st.integers(min_value=1, max_value=max_cols))
    cells = draw(
        st.lists(
            st.sampled_from(["0", "1"]),
            min_size=rows * cols,
            max_size=rows * cols,
        )
    )
    return [cells[r * cols : (r + 1) * cols] for r in range(rows)]


class TestNumIslandsProperties:
    @given(grid=random_grids())
    def test_invariant_under_180_rotation(self, grid: list[list[str]]) -> None:
        """Flood-fill connectivity doesn't care about the grid's orientation."""
        rotated = [row[::-1] for row in grid[::-1]]
        assert num_islands(grid) == num_islands(rotated)

    @given(grid=random_grids())
    def test_invariant_under_transpose(self, grid: list[list[str]]) -> None:
        transposed = [list(col) for col in zip(*grid, strict=True)]
        assert num_islands(grid) == num_islands(transposed)
