import collections
import copy
import functools
from typing import List

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook

WHITE, BLACK = range(2)

Coordinate = collections.namedtuple('Coordinate', ('x', 'y'))


def search_maze(maze: List[List[int]], s: Coordinate,
                e: Coordinate) -> List[Coordinate]:
    # DFS search starting from s coordinate
    # Terminal condition if current cell is e return True
    # Other one we want to skip 
    #   If current cell is seen
    #   If current cell is BLACK
    #   Coordinates are invalid
    # Recurse
    # If cell is WHITE, check adjacent neighbors x+1,y x-1,y, x,y+1, x,y-1
    # Fall through return False (by now you've "seen" all cells or only BLACK remain)

    def search_cell(cell, seen, path):
        if cell.x not in range(x_max) or cell.y not in range(y_max) or cell in seen or maze[cell.x][cell.y] == BLACK:
            return False
        seen.add(cell)
        if cell == e:
            nonlocal res
            res = path
            return True
        right = Coordinate(cell.x+1,cell.y)
        left = Coordinate(cell.x-1,cell.y)
        up = Coordinate(cell.x,cell.y-1)
        down = Coordinate(cell.x,cell.y+1)

        for coordinate in [right, left, up, down]:
            search_cell(coordinate, seen, path + [coordinate])
       
        return False

    seen = set()
    x_max = len(maze)
    y_max = len(maze[0])
    path = [s]
    res = []
    search_cell(s, seen, path)
    return res




def path_element_is_feasible(maze, prev, cur):
    if not ((0 <= cur.x < len(maze)) and
            (0 <= cur.y < len(maze[cur.x])) and maze[cur.x][cur.y] == WHITE):
        return False
    return cur == (prev.x + 1, prev.y) or \
           cur == (prev.x - 1, prev.y) or \
           cur == (prev.x, prev.y + 1) or \
           cur == (prev.x, prev.y - 1)


@enable_executor_hook
def search_maze_wrapper(executor, maze, s, e):
    s = Coordinate(*s)
    e = Coordinate(*e)
    cp = copy.deepcopy(maze)

    path = executor.run(functools.partial(search_maze, cp, s, e))

    if not path:
        return s == e

    if path[0] != s or path[-1] != e:
        raise TestFailure('Path doesn\'t lay between start and end points')

    for i in range(1, len(path)):
        if not path_element_is_feasible(maze, path[i - 1], path[i]):
            raise TestFailure('Path contains invalid segments')

    return True


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('search_maze.py', 'search_maze.tsv',
                                       search_maze_wrapper))
