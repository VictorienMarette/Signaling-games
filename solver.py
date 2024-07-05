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
        #Calcule des utilité en fionction de A et T, s donné pour les deux joueur
        vectorized_U_r = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        reciver_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U_r, (len_A,len_T))

        vectorized_U = np.vectorize(lambda i,j: U(A[int(i)], s, T[int(j)]))
        sender_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U, (len_A,len_T))
    
        
        #On cherches l'ensembles startegies fesable selon une certaine croyance
        fisable_action_distribution_per_signal[s] = {}

        # Générer tous les sous-ensembles de A pour verfier si 
        # il y a des croyance ou le receveur est indférant entre plusieurs actions
        subsets = list(powerset(range(len_A)))
        subsets.remove(())
        for subset in subsets:
            # On le verifie avec de la programation lineaire

            #Matrice d'ont on veut maximiser le roduit scalaire, inutile pour l'instant
            c = [i for i in range(len_T)]

            #contraintes de negativités
            one_column_matrix = np.zeros((len_A, len_A))
            one_column_matrix[:, subset[0]] = 1
            A_ub = (np.identity(len_A) - one_column_matrix) @ reciver_utility_per_action_per_signal[s]
            
            b_ub = one_column_matrix = np.zeros(len_A)

            #Contrainte sd'égalités
            action_selec_matrix = np.zeros((len_A,len_A))
            for i in subset:
                action_selec_matrix[i][i] = 1
            utility_eq = action_selec_matrix @ A_ub
            A_eq = np.vstack((utility_eq,np.ones((1,len_T))))

            b_eq= np.zeros(len_A)
            b_eq= np.append(b_eq, 1)    

            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
            
            #Si cest possible on cherche les actions a qui on peut donner une proba nul
            if result.success:
                fisable_action_distribution_per_signal[s][subset] = []
                
                #On regarde tout les combinaisons de proba nul possible
                Tsubsets = list(powerset(range(len_T)))
                Tsubsets.remove(())
                for tsubset in Tsubsets:
                    A_eq_T_subset = np.copy(A_eq)
                    for i in tsubset:
                        pass

                    
                    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
                    if result.success:
                        fisable_action_distribution_per_signal[s][subset].append(tsubset)
                    
            

        
    return fisable_action_distribution_per_signal

a,b,c = solve_PBE(T,S,A,U,U_r)