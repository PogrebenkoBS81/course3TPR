from chooser_statistician import ChooserStatistician
from couple_chooser import CoupleChooser
from couple_chooser_grapher import CoupleChooserGrapher, Result


class Menu:
    def __init__(self, separator):
        self.separator = separator
        self._m_iterations_list = ""
        self._n_size_list = ""
        self._d_criterion_list = ""

    @property
    def separator(self):
        return self._separator

    @property
    def m_iterations_list(self):
        return self._m_iterations_list

    @property
    def n_size_list(self):
        return self._n_size_list

    @property
    def d_criterion_list(self):
        return self._d_criterion_list

    @separator.setter
    def separator(self, separator):
        self._separator = separator

    @m_iterations_list.setter
    def m_iterations_list(self, m_iterations_raw):
        self._m_iterations_list = self._split_to_int(m_iterations_raw, self.separator)

    @n_size_list.setter
    def n_size_list(self, n_size_raw):
        self._n_size_list = self._split_to_int(n_size_raw, self.separator)

    @d_criterion_list.setter
    def d_criterion_list(self, d_criterion_raw):
        self._d_criterion_list = self._split_to_int(d_criterion_raw, self.separator)

    def _get_iterations_param(self):
        self.m_iterations_list = input("Введіть ваші 'M' через кому (M > 1): ")

    def _get_size_param(self):
        self.n_size_list = input("Введіть ваші 'N' через кому (N > 100): ")

    def _get_criterion_param(self):
        self.d_criterion_list = input("Введіть ваші 'd' через кому (d >= 0): ")

    def _calculate_params(self):
        results = []
        # calculate all combination of parameters
        for iterations in self.m_iterations_list:
            for size in self.n_size_list:
                for criterion in self.d_criterion_list:
                    results.append(
                        Result(
                            iterations,
                            size,
                            criterion,
                            ChooserStatistician(iterations).get_chooser_p(CoupleChooser(size, criterion))
                        )
                    )

        return results

    def _handle_a_task(self):
        self._get_iterations_param()
        self._get_size_param()
        self.d_criterion_list = self.separator.join(["0", "5"])

        self._handle_p_n_graph()

    def _handle_b_task(self):
        self._get_iterations_param()
        self.n_size_list = self.separator.join(["1000"])
        self.d_criterion_list = self.separator.join(["4"])

        self._handle_p_m_graph()

    def _handle_p_n_graph(self):
        CoupleChooserGrapher.build_p_n_graph(self._calculate_params())

    def _handle_p_m_graph(self):
        CoupleChooserGrapher.build_p_m_graph(self._calculate_params())

    def _handle_custom_graph_dialog(self):
        choice = input(
            "--------------------------------------------------------\n"
            "Оберіть тип графіку з довільними параметрами:\n"
            "1) Щоб побудувати графік залежності ймовірності 'p' від числа претендентів 'N' введіть 1.\n"
            "2) Щоб побудувати графік залежності ймовірності 'p' від числа експериментів 'M' введіть 2.\n"
            "Ваш вибір: "
        ).strip()

        self._get_iterations_param()
        self._get_size_param()
        self._get_criterion_param()

        if choice == "1":
            self._handle_p_n_graph()
        elif choice == "2":
            self._handle_p_m_graph()
        else:
            print("Неможлива опція, спробуйте обрати знов.")

    def start(self):
        while True:
            choice = input(
                "--------------------------------------------------------\n"
                "1) Щоб побудувати графік залежності ймовірності 'p'"
                "від числа претендентів N (при фіксованих поступках d=0 та d=5, введіть 1. \n"
                "2) Щоб побудувати графік залежності ймовірності 'p'"
                "від числа експериментів 'M' в серії (при фіксованих значеннях N=1000 та d=4, введіть 2.\n"
                "3) Щоб побудувати графік з довільними параметрами введіть 3.\n"
                "4) Щоб вийти з програми введіть 4.\n"
                "Ваш вибір: "
            ).strip()

            try:
                if choice == "1":
                    self._handle_a_task()
                elif choice == "2":
                    self._handle_b_task()
                elif choice == "3":
                    self._handle_custom_graph_dialog()
                elif choice == "4":
                    break
                else:
                    print("Неможлива опція, спробуйте обрати знов.")
            except ValueError as e:
                print("\n!!!!!!!!!!!!!!\n"
                      "Виникла помилка! Перевірте своі вхідні данні та повторіть спробу.\n"
                      "Помилка: " + str(e) +
                      "\n!!!!!!!!!!!!!!")

    @staticmethod
    def _split_to_int(raw_input, separator):
        return [int(x) for x in raw_input.split(separator)]
