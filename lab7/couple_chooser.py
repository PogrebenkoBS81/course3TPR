import math
from random import uniform


class CoupleChooser:
    LOW_BOUND = 160
    HIGH_BOUND = 190

    def __init__(self, n_size, d_criterion):
        self.n_size = n_size
        self.d_criterion = d_criterion

        self.rng_list = None

    @property
    def n_size(self):
        return self._n_size

    @property
    def d_criterion(self):
        return self._d_criterion

    @property
    def rng_list(self):
        return self._rng_list

    @n_size.setter
    def n_size(self, n_size):
        if not n_size > 100:
            raise ValueError("Matrix size should be > 100")

        self._n_size = n_size

    @d_criterion.setter
    def d_criterion(self, d_criterion):
        if not d_criterion >= 0:
            raise ValueError("Criterion should be > 0")

        self._d_criterion = d_criterion

    @rng_list.setter
    def rng_list(self, rng_list):
        self._rng_list = rng_list

    def _generate_list(self):
        self.rng_list = [uniform(self.LOW_BOUND, self.HIGH_BOUND) for _ in range(self.n_size)]

    def _is_top_in_range(self, val, low_idx, high_idx):
        return val > max(self.rng_list[low_idx:high_idx])

    def _search_top_in_range(self, begin_idx, end_idx):
        for idx in range(begin_idx, end_idx, 1):
            if self._is_top_in_range(self.rng_list[idx], 0, idx):
                return self.rng_list[idx]

        return self.rng_list[end_idx - 1]

    def _get_win_criterion(self):
        return max(self.rng_list)

    def _get_xj_idx(self):
        return int(self.n_size / math.e) + 1

    def _get_xj(self):
        return self._search_top_in_range(self._get_xj_idx(), self.n_size)

    def is_win(self):
        self._generate_list()
        xj = self._get_xj()

        return self._get_win_criterion() - xj <= self.d_criterion
