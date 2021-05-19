import itertools

import numpy as np

from util import Dot, Line


# TODO: code is too difficult to read. Find a way to simplify it.
#  Solid is broken few times here, and in the menu. No time to fix it.
class GameMatrix:
    LOW_BOUND = -20
    HIGH_BOUND = 20

    def __init__(self, m_size, n_size, rng_list):
        self.m_size = m_size
        self.n_size = n_size

        self.rng_list = rng_list

    def __eq__(self, other):
        return self.m_size == other.m_size \
               and self.n_size == other.n_size \
               and (self.rng_list == other.rng_list).all()

    @classmethod
    def rng_matrix(cls, m_size, n_size):
        # Generate random matrix with values from -20 to 20, size of m rows n columns.
        return cls(m_size, n_size, np.random.randint(cls.LOW_BOUND, cls.HIGH_BOUND, (m_size, n_size)))

    @classmethod
    def from_matrix(cls, matrix):
        # Check if given matrix - valid.
        m, n = GameMatrix._check_shape(matrix)

        return cls(m, n, matrix)

    @property
    def m_size(self):
        return self._m_size

    @property
    def n_size(self):
        return self._n_size

    @property
    def rng_list(self):
        return self._rng_list

    @m_size.setter
    def m_size(self, m_size):
        if not m_size > 0:
            raise ValueError("Matrix rows number should be > 0")

        self._m_size = m_size

    @n_size.setter
    def n_size(self, n_size):
        if not n_size > 0:
            raise ValueError("Matrix columns number should be > 0")

        self._n_size = n_size

    @rng_list.setter
    def rng_list(self, rng_list):
        m, n = GameMatrix._check_shape(rng_list)

        self.m_size = m
        self.n_size = n

        self._rng_list = rng_list

    @staticmethod
    def _check_shape(matrix):
        matrix_shape = matrix.shape

        if len(matrix_shape) != 2:
            raise ValueError("Can work only with 2D matrices")

        return matrix_shape[0], matrix_shape[1]

    def _is_row_submissive(self, check_row):
        # Check if there is a row, where all values are greater than the corresponding values of the given row.
        return np.any([np.all(check_row < row) for row in self.rng_list])

    def _is_column_dominant(self, check_column):
        # Check if there is a column, where all values are smaller than the corresponding values of the given column.
        return np.any([np.all(check_column > column) for column in self.rng_list.transpose()])

    def filter_submissive_rows(self):
        non_submissive = np.apply_along_axis(
            lambda x: not self._is_row_submissive(x),  # Return True only if row is not submissive.
            1,  # Apply on each row.
            self.rng_list  # Apply on rng_list matrix.
        )
        # Return all non-submissive rows.
        self.rng_list = self.rng_list[non_submissive]

    def filter_dominant_columns(self):
        non_dominant = np.apply_along_axis(
            lambda x: not self._is_column_dominant(x),  # Return True only if row is not dominant.
            0,  # Apply on each column.
            self.rng_list  # Apply on rng_list matrix.
        )

        # Return all non-dominant columns.
        self.rng_list = self.rng_list[:, non_dominant]

    def get_high_cost_idx(self):
        # The row indices of the largest value in each column.
        row_max_ids = np.argmax(self.rng_list, axis=0)
        # Get min value of max values of columns.
        min_of_max = np.argmin(
            self.rng_list[
                row_max_ids,  # Get all max values
                np.arange(self.n_size),  # Iterate over every column.
            ]
        )

        return row_max_ids[min_of_max], min_of_max

    def get_high_cost(self):
        m, n = self.get_high_cost_idx()
        return self.rng_list[m][n]

    def get_low_cost_idx(self):
        # The column indices of the lowest value in each row.
        column_min_ids = np.argmin(self.rng_list, axis=1)
        # Get max value of min values of columns.
        max_of_min = np.argmax(
            self.rng_list[
                np.arange(self.m_size),  # Iterate over every row.
                column_min_ids,  # And get min values.
            ]
        )

        return max_of_min, column_min_ids[max_of_min]

    def get_low_cost(self):
        m, n = self.get_low_cost_idx()

        return self.rng_list[m][n]

    def get_saddle_point_idx(self):
        low_n, low_m = self.get_low_cost_idx()

        if (low_n, low_m) == self.get_high_cost_idx():
            return low_n, low_m

        return None, None

    def get_saddle_point(self):
        m, n = self.get_saddle_point_idx()

        if m is None or n is None:
            return None

        return self.rng_list[m][n]

    def get_lines(self):
        lines = []
        # Form dots from first 2 lines of matrix.
        for idx, pair in enumerate(self.rng_list.transpose()):
            dot1 = Dot(1, pair[0])
            dot2 = Dot(2, pair[1])

            lines.append(Line(dot1, dot2, f"line{idx}"))

        return lines

    def cut_matrix(self, rows=None, columns=None):
        old_rows, old_columns = self.rng_list.shape

        if rows is None:
            rows = old_rows

        if columns is None:
            columns = old_columns

        self.rng_list = self.rng_list[:rows, :columns]

    @staticmethod
    def matrix_from_lines(line1, line2):
        return np.array([
            [line1.dot1.y, line2.dot1.y],
            [line1.dot2.y, line2.dot2.y],
        ])

    @staticmethod
    def get_coefficients(lines):
        p1 = (lines[1][1] - lines[1][0]) / (lines[0][0] + lines[1][1] - lines[0][1] - lines[1][0])
        p2 = 1 - p1
        q1 = (lines[1][1] - lines[0][1]) / (lines[0][0] + lines[1][1] - lines[0][1] - lines[1][0])
        q2 = 1 - q1
        v = ((lines[1][1] * lines[0][0]) - (lines[0][1] * lines[1][0])) / \
            (lines[0][0] + lines[1][1] - lines[0][1] - lines[1][0])

        return p1, p2, q1, q2, v

    # TODO: add normal doc with """ """
    @staticmethod
    def is_valid_intersection(intersection):
        # If lines are parallel.
        if intersection is None:
            return False
        # If intersection in outer zone of the graph - ignore it
        if not (1 < intersection[0] < 2):
            return False

        return True  # If found intersection is fine for us.

    @staticmethod
    def get_first_intersection(lines):
        # Since we need to get first intersection starting from bottom,
        # we need to find the intersection with lowest Y, that inside our graph "window"
        def get_intersection(lines_tuple):
            line1, line2 = lines_tuple[0], lines_tuple[1]
            intersection = line1.line_intersection(line2)

            if not GameMatrix.is_valid_intersection(intersection):
                return float("inf")

            # Return Y of the intersection
            return intersection[1]

        result = min(
            itertools.combinations(lines, 2),
            key=get_intersection  # Find intersection with the lowest Y.
        )
        res_intersection = result[0].line_intersection(result[1])

        if not GameMatrix.is_valid_intersection(res_intersection):
            return None

        return result
