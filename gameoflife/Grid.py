import abc

from enum import Enum
from typing import List
from PIL import Image, ImageDraw

# ----------------------------------------------------------------------------------------------------------------------


class GridType(Enum):
    WRAPPING = 1
    ESCAPING = 2

# ----------------------------------------------------------------------------------------------------------------------


class Grid:
    """
    Our Game space
    """

    def __init__(self, factory_, x_: int, y_: int, grid_: List[List[int]] = None):
        self.m_width = x_
        self.m_height = y_
        self.m_factory = factory_

        if grid_ is None:
            self.m_grid = [[0 for _ in range(x_)] for _ in range(y_)]
        else:
            self.m_grid = grid_

    def __getitem__(self, key_: int) -> List[int]:
        return self.m_grid[key_]

    def __str__(self):
        return self.m_grid.__str__()

    def idx(self, x_: int, y_: int) -> int:
        return self[y_][x_]

    def set(self, x_: int, y_: int, to_) -> None:
        self.m_grid[y_][x_] = to_

    def fill(self) -> None:
        """
        Test func
        """
        i = 1
        for x in range(self.m_height):
            for y in range(self.m_width):
                self.m_grid[x][y] = i
                i += 1

    @abc.abstractmethod
    def sum(self, x_, y_) -> int:
        pass

    def render(self) -> Image:
        image = Image.new("RGB", (self.m_width * 10, self.m_height * 10), "black")
        draw = ImageDraw.Draw(image)

        for y in range(self.m_height):
            for x in range(self.m_width):
                if self.m_grid[y][x] == 1:
                    draw.rectangle((x * 10, y * 10, (x * 10) + 10, (y * 10) + 10), fill='red')

        return image


# ----------------------------------------------------------------------------------------------------------------------


class WrappingGrid(Grid):
    def __init__(self, factory_, x_: int, y_: int, grid_: List[List[int]] = None):
        super().__init__(factory_, x_, y_, grid_)

    def next_x(self, x_: int) -> int:
        if x_ >= self.m_width or x_ < 0:
            raise ValueError(f"{x_} out of bounds 0..{self.m_width}")
        elif x_ == self.m_width - 1:
            return 0
        else:
            return x_ + 1

    def prev_x(self, x_: int) -> int:
        if x_ < 0 or x_ >= self.m_width:
            raise ValueError(f"{x_} out of bounds 0..{self.m_width}")
        elif x_ == 0:
            return self.m_width - 1
        else:
            return x_ - 1

    def next_y(self, y_: int) -> List[int]:
        if y_ >= self.m_height or y_ < 0:
            raise ValueError(f"{y_} out of bounds 0..{self.m_height}")
        elif y_ == self.m_height - 1:
            return self.m_grid[0]
        else:
            return self.m_grid[y_ + 1]
        pass

    def prev_y(self, y_: int) -> List[int]:
        if y_ >= self.m_height or y_ < 0:
            raise ValueError(f"{y_} out of bounds 0..{self.m_height}")
        elif y_ == 0:
            return self.m_grid[self.m_height - 1]
        else:
            return self.m_grid[y_ - 1]
        pass

    def sum(self, x_, y_) -> int:
        rows = [self.prev_y(y_), self.m_grid[y_], self.next_y(y_)]
        cols = [self.prev_x(x_), x_, self.next_x(x_)]

        count = 0

        for row_i, row in enumerate(rows):
            for col_i, col in enumerate(cols):
                if row_i == 1 and col_i == 1:
                    continue
                if row[col] == 1:
                    count += 1

        return count

# ----------------------------------------------------------------------------------------------------------------------


class EscapingGrid(Grid):
    def __init__(self, factory_, x_: int, y_: int, grid_: List[List[int]] = None):
        super().__init__(factory_, x_, y_, grid_)
        self.m_empty = [0 for _ in range(x_)]

    def next_y(self, y_: int) -> List[int]:
        if y_ >= self.m_height or y_ < 0:
            raise ValueError(f"{y_} out of bounds 0..{self.m_height}")
        elif y_ == self.m_height - 1:
            return self.m_empty
        else:
            return self.m_grid[y_ + 1]
        pass

    def prev_y(self, y_: int) -> List[int]:
        if y_ >= self.m_height or y_ < 0:
            raise ValueError(f"{y_} out of bounds 0..{self.m_height}")
        elif y_ == 0:
            return self.m_empty
        else:
            return self.m_grid[y_ - 1]
        pass

    def sum(self, x_, y_) -> int:
        rows = [self.prev_y(y_), self.m_grid[y_], self.next_y(y_)]
        cols = [x_ - 1, x_, x_ + 1]

        count = 0

        for row_i, row in enumerate(rows):
            for col_i, col in enumerate(cols):
                if row_i == 1 and col_i == 1:
                    continue
                if 0 <= col < self.m_width:
                    if row[col] == 1:
                        count += 1

        return count


# ----------------------------------------------------------------------------------------------------------------------

class GridFactory:
    def __init__(self, type_: GridType):
        self.m_type = type_

    def from_list(self, l_: List[List[int]]) -> Grid:
        if self.m_type == GridType.WRAPPING:
            return WrappingGrid(self, len(l_[0]), len(l_), l_)
        else:
            return EscapingGrid(self, len(l_[0]), len(l_), l_)

    def from_xy(self, x_: int, y_: int) -> Grid:
        if self.m_type == GridType.WRAPPING:
            return WrappingGrid(self, x_, y_)
        else:
            return EscapingGrid(self, x_, y_)

# ----------------------------------------------------------------------------------------------------------------------
