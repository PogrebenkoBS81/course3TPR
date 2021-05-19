import math

import matplotlib.pyplot as plt
import numpy as np


class CoupleChooserGrapher:
    @staticmethod
    def _segregate_objects(values, criteria_func):
        segregated_objects = {}

        for v in values:
            criteria = criteria_func(v)

            if criteria not in segregated_objects:
                segregated_objects[criteria] = []

            segregated_objects[criteria].append(v)

        return segregated_objects

    @staticmethod
    def build_p_n_graph(results):
        CoupleChooserGrapher.build_graph(
            results,
            lambda x: x.size,
            lambda x: x.iterations,
            main_label="N size",
            subplot_title="M"
        )

    @staticmethod
    def build_p_m_graph(results):
        CoupleChooserGrapher.build_graph(
            results,
            lambda x: x.iterations,
            lambda x: x.size,
            main_label="M iterations",
            subplot_title="N"
        )

    @staticmethod
    def choose_subplot(plots_num):
        if plots_num < 3:
            return plots_num, 1

        return 2, math.ceil(plots_num / 2)

    @staticmethod
    def build_graph(results, main_criterion_func, secondary_criterion_func, main_label="", subplot_title=""):
        # TODO: Rewrite all this mess...
        # create map: {"<d_criterion>" : [<results with that d_criterion>]}
        iteration_results = CoupleChooserGrapher._segregate_objects(results, secondary_criterion_func)
        rows, columns = CoupleChooserGrapher.choose_subplot(len(iteration_results))
        fig, _ = plt.subplots(rows, columns)
        plots = zip(iteration_results.items(), fig.axes)

        for (s_key, s_values), ax in plots:
            criteria_results = CoupleChooserGrapher._segregate_objects(s_values, lambda x: x.criterion)

            for c_key, c_value in criteria_results.items():
                c_value.sort(key=main_criterion_func)

                x_list = np.array([main_criterion_func(x) for x in c_value])
                y_list = np.array([x.chance for x in c_value])
                y_mean = sum(y_list) / len(y_list)

                ax.plot(x_list, y_list, label=f"d={c_key}")
                ax.plot(x_list, [y_mean] * len(y_list), label=f"d={c_key}, mean={y_mean:.4}", linestyle='dashed')

                ax.set_xlabel(main_label)
                ax.set_ylabel('p chance')
                ax.set_title(f"{subplot_title}={s_key}")

                ax.grid(b=True, which='major', linestyle='-')
                ax.minorticks_on()
                ax.legend()

        plt.tight_layout()
        plt.show()


class Result:
    def __init__(self, iterations, size, criterion, chance):
        self.iterations = iterations
        self.size = size
        self.criterion = criterion
        self.chance = chance

    @property
    def chance(self):
        return self._chance

    @chance.setter
    def chance(self, chance):
        if chance < 0:
            raise ValueError("Probability cannot be lover than 0!")

        self._chance = chance
