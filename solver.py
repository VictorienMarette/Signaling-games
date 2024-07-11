import numpy as np
from more_itertools import powerset
from scipy.optimize import linprog

import sympy as sp

from games.RPS_2_A import *


def solve_PBE_frac(T,S,A,U,U_r):
    #Calcule les utilités des deux joueurs en fonction de S, A et T 
    sender_utility_per_action_per_signal_per_state, reciver_utility_per_action_per_signal_per_state \
        = calculate_utility_fonctions(T,S,A,U,U_r)

    # Calcule des actions indifférentes du receveur avec un prior arbitraire
    indifferent_actions = get_indifferent_actions(T,S,A, reciver_utility_per_action_per_signal_per_state)

    return indifferent_actions
    

def calculate_utility_fonctions(T,S,A,U,U_r):
    len_A = len(A)
    len_T = len(T)

    sender_utility_per_action_per_signal = {}
    reciver_utility_per_action_per_signal = {}

    for s in S:
        #Calcule les utilités des deux joueurs en fonction de S, A et T 
        vectorized_U = np.vectorize(lambda i,j: U(A[int(i)], s, T[int(j)]))
        sender_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U, (len_A,len_T))

        vectorized_U_r = np.vectorize(lambda i,j: U_r(A[int(i)], s, T[int(j)]))
        reciver_utility_per_action_per_signal[s] = np.fromfunction(vectorized_U_r, (len_A,len_T))

    return sender_utility_per_action_per_signal, reciver_utility_per_action_per_signal


def get_indifferent_actions(T,S,A, reciver_utility_fonction):
    # Calcule des actions indifférentes du receveur avec un prior arbitraire

    len_A = len(A)
    len_T = len(T)

    indifferent_actions_with_a_certain_prior = {}

    for s in S:        
        
        indifferent_actions_with_a_certain_prior[s] = {}

        # Générer tous les sous-ensembles de A pour vérifier s'il y a des croyances 
        # où le receveur est indifférent aux actions de ce sous-ensemble
        subsets = get_subsets(len_A)
        for subset in subsets:
            # On vérifie avec de la programmation linéaire

            # Matrice dont on veut maximiser le produit scalaire, inutile pour l'instant
            c = [i for i in range(len_T)]

            # Contraintes de négativité, on vérifie que les actions du sous-ensemble sont bien les meilleures
            A_ub, b_ub = A_ub_and_b_ub(len_A,s, subset, reciver_utility_fonction)

            # Contrainte d'égalité, on vérifie que les actions du sous-ensemble donnent la même utilité 
            # et que la somme des probabilités est 1
            A_eq, b_eq = A_eq_and_b_eq(len_T,len_A, subset, A_ub)    

            result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None))
            
            # Si c'est possible, on cherche les actions à qui on peut donner une probabilité nulle 
            # dans les cas où les actions du sous-ensemble sont indifférentes
            if result.success:
                indifferent_actions_with_a_certain_prior[s][subset] = [()]
                
                # On regarde toutes les combinaisons d'états où une probabilité nulle est possible
                subsets2 = get_subsets(len_T)
                while len(subsets2) != 0:
                    subset2 = subsets2[0]

                    # On ajoute des contraintes d'égalité au problème précédent, 
                    # on vérifie que les probabilités des états de subset2 sont nulles
                    A_eq2, b_eq2 = A_eq2_and_b_eq2(A_eq, b_eq, len_T, subset2)

                    result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq2 , b_eq=b_eq2 , bounds=(0, None))
                    
                    # Si c'est possible, on ajoute les états possibles dans la liste
                    if result.success:
                        indifferent_actions_with_a_certain_prior[s][subset].append(subset2)
                        # On supprime les sous ensembles de subset 2 dans subsets2
                        subsets2 = list(filter(lambda x: not set(x).issubset(set(subset2)), subsets2))
                    else:
                        #On supprime subset2 dans subsets2
                        subsets2.remove(subset2)
        
    return indifferent_actions_with_a_certain_prior


def get_subsets(n):
    # Génère les sous-ensembles de {0, ..., n-1}
    subsets = list(powerset(range(n)))
    subsets.remove(())
    subsets.reverse()
    return subsets


def A_ub_and_b_ub(len_A,s, subset, reciver_utility_fonction):

    one_column_matrix = np.zeros((len_A, len_A))
    one_column_matrix[:, subset[0]] = 1
    A_ub = (np.identity(len_A) - one_column_matrix) @ reciver_utility_fonction[s]
    
    b_ub = one_column_matrix = np.zeros(len_A)
    
    return A_ub, b_ub


def A_eq_and_b_eq(len_T,len_A, subset, A_ub):
    action_selec_matrix = np.zeros((len_A,len_A))
    for i in subset:
        action_selec_matrix[i][i] = 1
    utility_eq = action_selec_matrix @ A_ub
    A_eq = np.vstack((utility_eq,np.ones((1,len_T))))

    b_eq= np.zeros(len_A)
    b_eq= np.append(b_eq, 1)

    return A_eq, b_eq


def A_eq2_and_b_eq2(A_eq, b_eq, len_T, subset):
    A_eq2 = np.copy(A_eq)
    b_eq2 = np.copy(b_eq)

    for i in subset:
        addedligne = np.zeros((1,len_T))
        addedligne[0][i] = 1
        A_eq2 = np.vstack((A_eq2,addedligne))

        b_eq2 = np.append(b_eq2, 0)

    return A_eq2, b_eq2


print(solve_PBE_frac(T,S,A,U,U_r))
