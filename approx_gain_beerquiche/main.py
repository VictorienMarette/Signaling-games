import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import sys
sys.path.insert(1, '/home/victorien/Documents/recherche/HEC/Signaling-games/games')
from beerquiche import *



#Calcule du gain maximum de l'émetteur à p_w fixe
def max_gain(p_w, print_mediator=False):
    return 2



#Affichage
fig, ax = plt.subplots()

ax.plot([0.5,1], [1.5,1], color='red')

ax.plot([0.5,1], [2.5,1], color='blue')

ax.plot([0,0.5], [3,2.5], color='green')

X = np.linspace(0.5, 1, 200)
Y = [max_gain(x) for x in X]
ax.plot(X, Y, color='green')

# Define custom legend patches
blue_patch = Patch(color='blue', label=r'Signaling with Commitment')
red_patch = Patch(color='red', label=r'PBE')
green_patch = Patch(color='green', label=r'Communication equilibrium')

# Add the custom legend
plt.legend(handles=[red_patch,blue_patch, green_patch])


# Set plot limits
ax.set_ylim([0, 3.5])


# Set labels
ax.set_xlabel('P(W)')
ax.set_ylabel('Mean gain')


plt.show()