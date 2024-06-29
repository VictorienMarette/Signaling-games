import numpy as np
from more_itertools import powerset
from scipy.optimize import linprog

from games.RPS_3_A_1_S import *


# sans doute nessesité d utiliser des fractions
def solve_PBE(T,S,A,U,U_r):
    len_A = len(A)
    len_T = len(T)

    reciver_utility_per_action_per_signal = {}
    sender_utility_per_action_per_signal = {}
    fisable_action_distribution_per_signal = {}

    for s in S:

        vectorized_U_r = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        reciver_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U_r, (len_A,len_T))

        vectorized_U = np.vectorize(lambda i,j: U(A[int(i)], s, T[int(j)]))
        sender_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U, (len_A,len_T))
    
        fisable_action_distribution_per_signal[s] = {}
        # Générer tous les sous-ensembles de A
        subsets = list(powerset(range(len_A)))
        subsets.remove(())
        for subset in subsets:
            print(subset)

            c = [i for i in range(len_T)]

            one_column_matrix = np.zeros((len_A, len_A))
            one_column_matrix[:, subset[0]] = 1
            A_ub = (np.identity(len_A) - one_column_matrix) @ reciver_utility_per_action_per_signal[s]
            print(A_ub)
            
            b_ub = one_column_matrix = np.zeros(len_A)

            action_selec_matrix = np.zeros((len_A,len_A))
            for i in subset:
                action_selec_matrix[i][i] = 1
            utility_eq = action_selec_matrix @ A_ub
            A_eq = np.vstack((utility_eq,np.ones((1,len_T))))

            b_eq= np.zeros(len_A)
            b_eq= np.append(b_eq, 1)    

            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
            #print(result.x)
            fisable_action_distribution_per_signal[s][subset] = result.success
        
    return reciver_utility_per_action_per_signal, fisable_action_distribution_per_signal, sender_utility_per_action_per_signal

a,b,c = solve_PBE(T,S,A,U,U_r)