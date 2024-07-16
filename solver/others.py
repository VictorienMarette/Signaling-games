import numpy as np
import sympy as sp


def calculate_utility_fonctions(T,S,A,U,U_r):
    len_A = len(A)
    len_T = len(T)

    sender_utility_per_action_per_signal_per_state = {}
    reciver_utility_per_action_per_signal_per_state = {}

    for s in S:
        #Calcule les utilités des deux joueurs en fonction de S, A et T 
        vectorized_U = np.vectorize(lambda i,j: sp.Rational((U(A[int(i)], s, T[int(j)]))))
        sender_utility_per_action_per_signal_per_state[s] = np.fromfunction(vectorized_U, (len_A,len_T))

        vectorized_U_r = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        reciver_utility_per_action_per_signal_per_state[s] = np.fromfunction(vectorized_U_r, (len_A,len_T))

    return sender_utility_per_action_per_signal_per_state, reciver_utility_per_action_per_signal_per_state