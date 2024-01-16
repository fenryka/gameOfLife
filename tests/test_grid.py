import pytest
import pprint

from gameoflife.Grid import Grid, WrappingGrid


class TestGrid:
    def test_we_can_test(self):
        grid = Grid(5, 5)
        assert (grid[0][0] == 0)

    def test_next_x(self):
        grid = WrappingGrid(5, 5)
        assert (grid.next_x(0) == 1)
        assert (grid.next_x(1) == 2)
        assert (grid.next_x(2) == 3)
        assert (grid.next_x(3) == 4)
        assert (grid.next_x(4) == 0)

    def test_next_y(self):
        grid = WrappingGrid(3, 2)
        grid.set(0, 0, 1)
        grid.set(1, 0, 2)
        grid.set(2, 0, 3)
        grid.set(0, 1, 4)
        grid.set(1, 1, 5)
        grid.set(2, 1, 6)

        assert (grid.next_y(0) == [4, 5, 6])
        assert (grid.next_y(1) == [1, 2, 3])
        with pytest.raises(ValueError):
            grid.next_y(2)

    def test_sum(self):
        grid = WrappingGrid(5, 5)
        grid.set(1, 3, 1)
        grid.set(3, 3, 1)
        grid.set(2, 1, 1)
        grid.set(2, 2, 1)
        grid.set(2, 3, 1)

        pp = pprint.PrettyPrinter(indent=2)
        print()
        pp.pprint(grid.m_grid)

        assert (grid.sum(0, 0) == 0)
        assert (grid.sum(1, 0) == 1)
        assert (grid.sum(2, 0) == 1)
        assert (grid.sum(3, 0) == 1)
        assert (grid.sum(4, 0) == 0)

        assert (grid.sum(0, 1) == 0)
        assert (grid.sum(1, 1) == 2)
        assert (grid.sum(2, 1) == 1)
        assert (grid.sum(3, 1) == 2)
        assert (grid.sum(4, 1) == 0)

        assert (grid.sum(0, 2) == 1)
        assert (grid.sum(1, 2) == 4)
        assert (grid.sum(2, 2) == 4)
        assert (grid.sum(3, 2) == 4)
        assert (grid.sum(4, 2) == 1)

        assert (grid.sum(0, 3) == 1)
        assert (grid.sum(1, 3) == 2)
        assert (grid.sum(2, 3) == 3)
        assert (grid.sum(3, 3) == 2)
        assert (grid.sum(4, 3) == 1)

        assert (grid.sum(0, 4) == 1)
        assert (grid.sum(1, 4) == 2)
        assert (grid.sum(2, 4) == 3)
        assert (grid.sum(3, 4) == 2)
        assert (grid.sum(4, 4) == 1)
