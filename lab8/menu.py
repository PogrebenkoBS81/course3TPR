import copy

import matplotlib.pyplot as plt
import numpy as np
from colorama import Back
from colorama import Fore
from colorama import Style

from game_matrix import GameMatrix


def initialize_checker(func):
    def wrapper(self=None):
        if self.game_mtx is None:
            print("Спочатку створіть матрицю!")
        else:
            return func(self)

    return wrapper


class Lab7:
    def __init__(self, game_mtx=None):
        self.game_mtx = None

        if game_mtx is not None:
            self.game_mtx = GameMatrix.from_matrix(game_mtx)

    def generate_random_mtx(self):
        n, m = self.get_input()
        self.game_mtx = GameMatrix.rng_matrix(n, m)
        self.print_game_mtx()

    # TODO: will take forever on large matrix. Find an algorithm to generate such matrix fast.
    def generate_random_saddle_mtx(self):
        n, m = self.get_input()

        if n > 10 or m > 10:
            raise ValueError("Для генерації матриці з сідловою точкою оберіть значення розмірів, що меньше 10.")

        while True:
            self.game_mtx = GameMatrix.rng_matrix(n, m)
            saddle = self.game_mtx.get_saddle_point()

            if saddle is not None:
                break

        self.print_game_mtx()

    @initialize_checker
    def print_game_mtx(self):
        print("\nПоточна матриця:")

        for i in range(self.game_mtx.m_size):
            for j in range(self.game_mtx.n_size):
                print(f"{self.game_mtx.rng_list[i][j]: < 5}", end=" ")

            print()

    @initialize_checker
    def print_full_info(self):
        Lab7.show_legend()
        print("Проаналізована матриця:")

        low_i, low_j = self.game_mtx.get_low_cost_idx()
        high_i, high_j = self.game_mtx.get_high_cost_idx()
        saddle_i, saddle_j = self.game_mtx.get_saddle_point_idx()

        for i in range(self.game_mtx.m_size):
            for j in range(self.game_mtx.n_size):
                if (i, j) == (saddle_i, saddle_j):
                    print(f"{Back.RED}{Fore.BLACK}{self.game_mtx.rng_list[i][j]: < 5}{Style.RESET_ALL}", end=" ")
                elif (i, j) == (high_i, high_j):
                    print(f"{Back.GREEN}{Fore.BLACK}{self.game_mtx.rng_list[i][j]: < 5}{Style.RESET_ALL}", end=" ")
                elif (i, j) == (low_i, low_j):
                    print(f"{Back.BLUE}{Fore.BLACK}{self.game_mtx.rng_list[i][j]: < 5}{Style.RESET_ALL}", end=" ")
                else:
                    print(f"{self.game_mtx.rng_list[i][j]: < 5}", end=" ")

            print(f"{Back.YELLOW}{Fore.BLACK}{np.min(self.game_mtx.rng_list[i]): < 5}{Style.RESET_ALL}")

        for val in np.max(self.game_mtx.rng_list, axis=0):
            print(f"{Back.YELLOW}{Fore.BLACK}{val: < 5}{Style.RESET_ALL}", end=" ")

        print(f"\nВерхня ціна гри: {self.game_mtx.get_high_cost()}\n"
              f"Нижня ціна гри: {self.game_mtx.get_low_cost()}\n"
              f"Сідлова точка: {self.game_mtx.get_saddle_point()}\n"
              )

    @initialize_checker
    def simplify_matrix(self):
        old_mtx = copy.deepcopy(self.game_mtx)
        # Simplify while possible (sometimes, removal of columns\rows can make new simplification possible).
        while True:
            self.game_mtx.filter_dominant_columns()
            self.game_mtx.filter_submissive_rows()

            if self.game_mtx == old_mtx:
                break

            old_mtx = copy.deepcopy(self.game_mtx)

    # TODO: refactor function to something nicer. Whole function is a HUGE mess.
    @initialize_checker
    def solve_graph(self):
        # TODO: save old game in adequate way.
        old_game = copy.deepcopy(self.game_mtx)

        print("Оберемо перші 2 рядка матриці, та проаналізуємо її:\n")
        self.game_mtx.cut_matrix(rows=2)
        self.print_full_info()

        if self.game_mtx.get_saddle_point() is not None:
            print("У результуючій матриці є сідлова точка, продовжувати роз'вязок неможливо. Згенеруйте нову матрицю.")
            return
        # Generate lines for graph solve.
        lines = self.game_mtx.get_lines()
        intersection = self.game_mtx.get_first_intersection(lines)

        if intersection is None:
            print("У результуючому графіку немає перетенів. Згенеруйте нову матрицю.")
            self.plot_lines(lines)
            return

        print(f"\nЛініі, перетин яких було взято для подальшої роботи: "
              f"{intersection[0].legend}, "
              f"{intersection[1].legend}")
        intersection_mtx = self.game_mtx.matrix_from_lines(intersection[0], intersection[1])
        print(f"Значення обранних ліній: \n{intersection_mtx[0]}\n{intersection_mtx[1]}")

        coefficients = self.game_mtx.get_coefficients(intersection_mtx)
        v = coefficients[4]
        print("\nПораховані коєфіцієенти:\n"
              f"p1={coefficients[0]:.4}\n"
              f"p2={coefficients[1]:.4}\n"
              f"q1={coefficients[2]:.4}\n"
              f"q2={coefficients[3]:.4}\n"
              f"v={v}\n"
              )

        high_cost, low_cost = self.game_mtx.get_high_cost(), self.game_mtx.get_low_cost()
        if low_cost < v < high_cost:
            print(f"Коєфіцієнт v ({v:.4}) знаходиться у межах {low_cost} < v < {high_cost} \n"
                  f"Отже ціна гри задовольняє умову і перевищує мінімальну ціну гри в чистих стратегіях. ")
        else:
            print(f"Коєфіцієнт v ({v:.4}) не знаходиться у межах {low_cost} < v < {high_cost}"
                  f"Отже ціна гри не задовольняє умову і не перевищує мінімальну ціну гри в чистих стратегіях. ")

        self.plot_lines(lines)
        self.game_mtx = old_game

    def run(self):
        while True:
            choice = input(
                "--------------------------------------------------------\n"
                "1) Щоб створити випадкову матрицю натисніть 1. \n"
                "2) Щоб створити матрицю де буде сідлова точка натисніть 2. \n"
                "3) Щоб показати поточну матрицю натисніть 3. \n"
                "4) Щоб проаналізувати поточну матрицю натисніть 4. \n"
                "5) Щоб спростити поточну матрицю натисніть 5. \n"
                "6) Щоб вирішити завдання графоаналітичніим методом, натисніть 6. \n"
                "Ваш вибір: "
            ).strip()

            try:
                if choice == "1":
                    self.generate_random_mtx()
                elif choice == "2":
                    self.generate_random_saddle_mtx()
                elif choice == "3":
                    self.print_game_mtx()
                elif choice == "4":
                    self.print_full_info()
                elif choice == "5":
                    self.simplify_matrix()
                elif choice == "6":
                    self.solve_graph()
            except ValueError as e:
                print("Виникла помилка. Перевірте своі вхідні данні та повторіть спробу.\n"
                      "Помилка: " + str(e) + "\n")

    @staticmethod
    def plot_lines(lines):
        for line in lines:
            plt.plot([line.dot1.x, line.dot2.x], [line.dot1.y, line.dot2.y], label=line.legend)

        plt.legend()
        plt.grid(alpha=0.1)
        plt.show()

    @staticmethod
    def get_input():
        n = int(input("Введіть кількість стовпців n матриці: "))
        m = int(input("Введіть кількість рядків m матриці: "))

        return m, n

    @staticmethod
    def show_legend():
        print("Жовтий стовпець - мінімальні значення кожного з рядів.\n"
              "Жовтий рядок - максимальні значення кожного з стовпців.\n"
              "Червоний колір комірки - сідлова точка.\n"
              "Зелений колір комірки - верхня ціна гри. \n"
              "Синій колір комірки - нижня ціна гри. \n")


if __name__ == "__main__":
    Lab7().run()
