class ChooserStatistician:
    def __init__(self, m_iterations):
        self.m_iterations = m_iterations

    @property
    def m_iterations(self):
        return self._m_iterations

    @m_iterations.setter
    def m_iterations(self, m_iterations):
        if not m_iterations > 1:
            raise ValueError("Number of iterations should be > 1")

        self._m_iterations = m_iterations

    def get_chooser_p(self, chooser):
        return sum(chooser.is_win() for _ in range(self.m_iterations)) / self.m_iterations
