import numpy as np
import sympy as sp

from others import *
from beliefs import *
from GeometricalObj import *
from visualisation import *

import sys
sys.path.insert(1, '/home/victorien/Documents/recherche/HEC/Signaling-games/games')
from RPS_3_A_1_S import *


def solve_PBE_frac(T,S,A,U,U_r):
    #Calcule les utilités des deux joueurs en fonction de S, A et T 
    sender_utility_vector_per_signal_per_action, reciver_utility_per_signal_per_state_per_action \
        = calculate_utility_fonctions(T,S,A,U,U_r)

    # Calcule des actions indifférentes du receveur avec un prior arbitraire
    indifferent_actions_beliefs = get_indifferent_actions(T,S,A, reciver_utility_per_signal_per_state_per_action)

    InterimPayoffPolygone_array = {}
    for s in S:
        InterimPayoffPolygone_array[s] = InterimPayoffPolygone(sender_utility_vector_per_signal_per_action[s],\
                                                                indifferent_actions_beliefs[s])

    show_all_InterimPayoffPolygone(InterimPayoffPolygone_array)
    
solve_PBE_frac(T,S,A,U,U_r)