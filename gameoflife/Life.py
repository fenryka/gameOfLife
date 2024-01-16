from enum import Enum
from gameoflife.Grid import Grid
from typing import List
from dataclasses import dataclass


class LifeResults(Enum):
    STATIC = 1
    OSCILLATING = 2
    UNSTABLE = 3


@dataclass
class EvaluateResults:
    result: LifeResults
    generations: int


class Life:
    @staticmethod
    def new_generation(curr_: Grid) -> Grid:
        """
        For reference, the rules:

            1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            2. Any live cell with two or three live neighbours lives on to the next generation.
            3. Any live cell with more than three live neighbours dies, as if by overpopulation.
            4.Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        """
        rtn = curr_.m_factory.from_xy(curr_.m_width, curr_.m_height)

        for x in range(rtn.m_width):
            for y in range(rtn.m_height):
                neighbours = curr_.sum(x, y)
                val = 0

                if curr_.idx(x, y) == 1:
                    """it's alive"""
                    if neighbours == 2 or neighbours == 3:
                        val = 1
                else:
                    """It's dead"""
                    if neighbours == 3:
                        val = 1

                rtn.set(x, y, val)

        return rtn

    @staticmethod
    def evaluate_n_generations(curr_: Grid, generations_: int, results_: List[Grid]) -> EvaluateResults:
        results_.append(curr_)

        for x in range(generations_):
            results_.append(Life.new_generation(results_[-1]))

            # easy test for static image
            if results_[-1].m_grid == results_[-2].m_grid:
                return EvaluateResults(LifeResults.STATIC, x)

        return EvaluateResults(LifeResults.UNSTABLE, -1)
