import numpy as np
from RPS_2_A import *
from more_itertools import powerset
from scipy.optimize import linprog


# sans doute nessesité d utiliser des fractions
def solve_PBE(T,S,A,U,U_r):
    #Il faut trouver les epsilons pour chaque s
    len_A = len(A)
    len_T = len(T)
    utility_per_action_per_state = []
    for s in S:
        vectorized_U = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        utility_per_action_per_state.append(np.fromfunction(vectorized_U, (len_A,len_T)))
    
    fisable_action_distribution = {}
    # Générer tous les sous-ensembles de A
    subsets = list(powerset(range(len_A)))
    for subset in subsets:
        c = [-1, -2]  # Coefficients for the objective function (negative for maximization)
        A = [[1, 1], [2, 1]]  # Coefficients for the inequalities
        b = [5, 8]  # RHS of the inequalities

        result = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

        fisable_action_distribution[subset] = result.success
    pass

print(solve_PBE(T,S,A,U,U_r))