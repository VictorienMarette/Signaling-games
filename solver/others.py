import numpy as np
import sympy as sp


def calculate_utility_fonctions(T,S,A,U,U_r):
    len_A = len(A)
    len_T = len(T)

    sender_utility_per_signal_per_action_per_signal = {}
    reciver_utility_per_action_per_signal_per_state = {}

    for s in S:
        sender_utility_per_signal_per_action_per_signal[s] = []
        for j in range(len_A):
            #Calcule les utilités des deux joueurs en fonction de S, A et T 
            vectorized_U = np.vectorize(lambda i: sp.Rational((U(A[j], s, T[int(i)]))))
            sender_utility_per_signal_per_action_per_signal[s].append(np.fromfunction(vectorized_U, (len_T,)))

        vectorized_U_r = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        reciver_utility_per_action_per_signal_per_state[s] = np.fromfunction(vectorized_U_r, (len_A,len_T))

    return sender_utility_per_signal_per_action_per_signal, reciver_utility_per_action_per_signal_per_state