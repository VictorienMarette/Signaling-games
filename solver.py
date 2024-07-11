import numpy as np
from more_itertools import powerset
from scipy.optimize import linprog

import sympy as sp

from games.RPS_2_A import *


def solve_PBE_frac(T,S,A,U,U_r):
    len_A = len(A)
    len_T = len(T)

    sender_utility_per_action_per_signal, reciver_utility_per_action_per_signal = calculate_utility_fonctions(T,S,A,U,U_r)

    return sender_utility_per_action_per_signal, reciver_utility_per_action_per_signal


def calculate_utility_fonctions(T,S,A,U,U_r):
    len_A = len(A)
    len_T = len(T)

    sender_utility_per_action_per_signal = {}
    reciver_utility_per_action_per_signal = {}

    for s in S:
        #Calcule des utilité en fonction de A et T, à s donné pour les deux joueur
        vectorized_U = np.vectorize(lambda i,j: U(A[int(i)], s, T[int(j)]))
        sender_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U, (len_A,len_T))

        vectorized_U_r = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        reciver_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U_r, (len_A,len_T))

    return sender_utility_per_action_per_signal, reciver_utility_per_action_per_signal


a,b = solve_PBE_frac(T,S,A,U,U_r)
print(a)
print(b)