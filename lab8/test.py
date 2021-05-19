import numpy as np

from menu import Lab7

print("----------------------------Full info test-------------------------")
test1 = Lab7(
    np.array([
        [-4, -4, -13, -1, -7],
        [-11, -14, -11, -17, -8],
        [3, 2, 2, -17, -10],
        [12, 14, 19, 11, 10],
        [9, 3, 9, 4, 11]
    ])
)
test1.print_full_info()

print("\n\n----------------------------Simplify matrix test-------------------------")
test2 = Lab7(
    np.array([
        [-9, 11, 14, 6, 2],
        [10, 17, 15, 8, 3],
        [18, 19, -4, -8, 15],
        [-10, 16, -17, -13, 19],
        [-19, 0, 2, -4, 13]
    ])
)
test2.print_full_info()
test2.simplify_matrix()
test2.print_full_info()

print("\n\n----------------------------Settle point test-------------------------")
test3 = Lab7(
    np.array([
        [-9, 0, -14, 16, 13],
        [5, 2, 5, 8, 3],
        [18, -5, -4, -8, 16],
        [3, -7, -5, -13, 20],
        [-19, 0, -2, -4, -14]
    ])
)
test3.print_full_info()

print("\n\n----------------------------Solve graph test-------------------------")
test4 = Lab7(
    np.array([
        [9, 18, 15, 3, -16],
        [3, 9, 3, -9, -2]
    ])
)
test4.print_full_info()
test4.solve_graph()
