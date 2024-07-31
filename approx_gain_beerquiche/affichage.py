import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


from approx_gain_in_CE import max_gain


#Affichage
fig, ax = plt.subplots()

ax.plot([0,0.5], [3,2.5], color='red')
ax.plot([0.5,1], [1.5,1], color='red')

ax.plot([0,0.5,1], [3,2.5,1], color='blue',linestyle='--')


X = np.linspace(0, 0.5, 10)
X1 = np.linspace( 0.5,1, 100)
X = np.concatenate((X,X1))
#que les cas non triviaux
X = np.delete(X, [0,109])
Y = []
i = 0
for x in X:
    print(i)
    Y.append(max_gain(x,number_initial_points = 6))
    i+=1
X= np.insert(X, 0, 0)
Y= np.insert(Y, 0, 3)
ax.plot(X, Y, color='green')

# Define custom legend patches
blue_patch = Patch(color='blue', label=r'Signaling with Commitment')
red_patch = Patch(color='red', label=r'PBE')
green_patch = Patch(color='green', label=r'Communication equilibrium estimé avec python')

# Add the custom legend
plt.legend(handles=[red_patch,blue_patch, green_patch])


# Set plot limits
ax.set_ylim([0, 3.5])


# Set labels
ax.set_xlabel('P(W)')
ax.set_ylabel('Mean gain')


plt.show()
