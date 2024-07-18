import numpy as np
import sympy as sp

from others import *
from beliefs import *

import games.RPS_2_A as yo


def solve_PBE_frac(T,S,A,U,U_r):
    #Calcule les utilités des deux joueurs en fonction de S, A et T 
    sender_utility_per_action_per_signal_per_state, reciver_utility_per_action_per_signal_per_state \
        = calculate_utility_fonctions(T,S,A,U,U_r)

    # Calcule des actions indifférentes du receveur avec un prior arbitraire
    indifferent_actions = get_indifferent_actions(T,S,A, reciver_utility_per_action_per_signal_per_state)

    return sender_utility_per_action_per_signal_per_state
    



#print(solve_PBE_frac(T,S,A,U,U_r))
