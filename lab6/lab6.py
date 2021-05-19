import copy
from random import randrange

from colorama import Fore
from colorama import Style
from colorama import Back


class Node:
    def __init__(self, value, parent):
        self._value = value
        self._parent = parent
        self._is_dye = False

    @property
    def value(self):
        return self._value

    @property
    def parent(self):
        return self._parent

    @property
    def is_dye(self):
        return self._is_dye

    @value.setter
    def value(self, value):
        self._value = value

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @is_dye.setter
    def is_dye(self, is_dye):
        self._is_dye = is_dye


class DynamicMatrix:
    def __init__(self, grid):
        self._grid_validation(grid)

        self._grid = grid
        self._node_matrix = None

    @property
    def grid(self):
        return self._grid

    @property
    def node_matrix(self):
        return self._node_matrix

    @grid.setter
    def grid(self, grid):
        self._grid = grid

    @node_matrix.setter
    def node_matrix(self, matrix):
        self._node_matrix = matrix

    def _prepare_matrix(self):
        n, m = self.get_grid_size()
        self.node_matrix = [[None for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                self.node_matrix[i][j] = Node(self.grid[i][j], None)

    def process_matrix(self):
        self._prepare_matrix()
        n, m = self.get_grid_size()

        # initialize first row
        for j in range(1, m):
            self.node_matrix[0][j] = Node(
                self.node_matrix[0][j - 1].value + self.node_matrix[0][j].value,
                self.node_matrix[0][j - 1]
            )
        # initialize first column
        for i in range(1, n):
            self.node_matrix[i][0] = Node(
                self.node_matrix[i - 1][0].value + self.node_matrix[i][0].value,
                self.node_matrix[i - 1][0]
            )
        # build dynamic matrix
        for i in range(1, n):
            for j in range(1, m):
                max_node = max(
                    self.node_matrix[i - 1][j],
                    self.node_matrix[i][j - 1],
                    self.node_matrix[i - 1][j - 1],
                    key=lambda x: x.value
                )

                self.node_matrix[i][j] = Node(
                    max_node.value + self.node_matrix[i][j].value,
                    max_node
                )

        return self.node_matrix

    def trace_path(self):
        n, m = self.get_grid_size()
        curr_node = self.node_matrix[n - 1][m - 1]

        path = ""
        separator = " -> "

        while curr_node is not None:
            curr_node.is_dye = True
            path += f" {curr_node.value}{separator}"
            curr_node = curr_node.parent

        return path[:-len(separator)]

    def get_grid_size(self):
        return len(self.grid), len(self.grid[0])

    @staticmethod
    def pretty_print_grid(grid):
        for row in grid:
            for value in row:
                print(f"{value: < 5}", end=" ")
            print()

    @staticmethod
    def pretty_print_mtx(mtx):
        for row in mtx:
            for node in row:
                if node.is_dye:
                    print(f"{Back.BLUE}{Fore.BLACK}{node.value: < 5}{Style.RESET_ALL}", end=" ")
                else:
                    print(f"{node.value: < 5}", end=" ")
            print()

    @staticmethod
    def _grid_validation(grid):
        if grid is None or len(grid) == 0 or len(grid[0]) == 0:
            raise ValueError('empty grid is provided!')

        it = iter(grid)
        the_len = len(next(it))

        if not all(len(lst) == the_len for lst in it):
            raise ValueError('not all rows have the same length!')

    @staticmethod
    def matrix_flip(m):
        temp_mtx = copy.deepcopy(m)

        for i in range(0, len(temp_mtx)):
            temp_mtx[i].reverse()

        return temp_mtx

    @staticmethod
    def get_random_grid(min_value, max_value, columns, rows):
        return [[randrange(min_value, max_value) for _ in range(columns)] for _ in range(rows)]


def solution():
    test1 = int(input())
    test2 = int(input())
    random_grid = DynamicMatrix.get_random_grid(-10, 10, test1, test2)
    flipped_grid = DynamicMatrix.matrix_flip(random_grid)

    mtx = DynamicMatrix(flipped_grid)
    processed_mtx = mtx.process_matrix()
    path = mtx.trace_path()

    unflipped_mtx = DynamicMatrix.matrix_flip(processed_mtx)

    print("Initial grid:")
    DynamicMatrix.pretty_print_grid(random_grid)
    print("\nCalculated dynamic matrix:")
    DynamicMatrix.pretty_print_mtx(unflipped_mtx)
    print("\nPath: \n", path)


solution()
