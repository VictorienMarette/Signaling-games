import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch

# Create a figure and a 3D axis
limite = 6
ylimite = 1
zlimite = 3

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plotwithtrans(x,y,z, color):
    # point 
    ax.scatter([3+x,-3+x], [-3+y,0+y], [0+z,3+z], color=color)

    #droite
    ax.plot([3+x,-3+x], [-3+y,0+y], [0+z,3+z], linewidth=3,alpha=0.5, color=color)

    #plan 1
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [-3+x, 0+y, 3+z], # Point B
        [-3+x, 0+y, 1.5*zlimite],# Point C
        [3+x, -3+y, 1.5*zlimite]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 2
    points = np.array([
    [3+x, -3+y, 0+z],  # Point A
    [-3+x, 0+y, 3+z], # Point B
    [-3+x, 1.5*ylimite, 3+z],# Point C
    [3+x, 1.5*ylimite, 0+z]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 3
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [1.5*limite, -3+y, 0+z], # Point B
        [1.5*limite, 1.5*ylimite, 0+z],# Point C
        [3+x, 1.5*ylimite, 0+z]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 4
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [1.5*limite, -3+y, 0+z], # Point B
        [1.5*limite, -3+y, 1.5*zlimite],# Point C
        [3+x, -3+y, 1.5*zlimite]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 5
    points = np.array([
        [-3+x, 0+y, 3+z],  # Point A
        [-3+x, 0+y, 1.5*zlimite], # Point B
        [-3+x, 1.5*ylimite, 1.5*zlimite],# Point C
        [-3+x, 1.5*ylimite, 3+z]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

#E pour le signal Rock s translation de (0,-1,-2)
plotwithtrans(0,-1,-1, "b")

#E pour le signal Paper s translation de (-2,0,-1)
plotwithtrans(-1,0,-1, "r")

#E pour le signal Paper s translation de (-2,0,-1)
plotwithtrans(-1,-1,0, "g")


"""#plot droites
ax.plot(np.array([3, 1]), np.array([-4, -3]), np.array([-2,-1]),linewidth=3, alpha=0.5, color="b")
ax.plot(np.array([-3, 1]), np.array([-1, -3]), np.array([1,-1]),linewidth=3, alpha=0.5, color="purple")

#plan 1



points = np.array([
        [3, -4, -2],  # Point A
        [1, -3, -1], # Point B
        [1, -3, 1.5*zlimite],# Point C
        [3, -4, 1.5*zlimite]  # Point D
    ])
x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x1, y1, z1))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor="b", edgecolor="b")
ax.add_collection3d(poly)

points = np.array([
        [-3, -1, 1],  # Point A
        [1, -3, -1], # Point B
        [1, -3, 1.5*zlimite],# Point C
        [-3, -1, 1.5*zlimite]  # Point D
    ])
x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x1, y1, z1))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor="purple", edgecolor="purple")
ax.add_collection3d(poly)


#plan 2
points = np.array([
    [-3, -1, 1],  # Point A
    [-5, 0, 2], # Point B
    [-5, 1.5*ylimite, 2],# Point C
    [-3, 1.5*ylimite, 1]  # Point D
])
x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x1, y1, z1))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor="r", edgecolor="r")
ax.add_collection3d(poly)


points = np.array([
    [3, -4, -2],  # Point A
    [1, -3, -1], # Point B
    [1, 1.5*ylimite, -1],# Point C
    [3, 1.5*ylimite, -2]  # Point D
])
x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x1, y1, z1))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor="b", edgecolor="b")
ax.add_collection3d(poly)


points = np.array([
    [-3, -1, 1],  # Point A
    [1, -3, -1], # Point B
    [1, 1.5*ylimite, -1],# Point C
    [-3, 1.5*ylimite, 1]  # Point D
])
x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x1, y1, z1))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor="purple", edgecolor="purple")
ax.add_collection3d(poly)"""



# Define custom legend patches
blue_patch = Patch(color='blue', label=r'$\mathcal{E}(Défilé \ aérien,.)$')
red_patch = Patch(color='red', label=r'$\mathcal{E}(Défilé \ maritime,.)$')
green_patch = Patch(color='green', label=r'$\mathcal{E}(Défilé \ terrestre,.)$')

# Add the custom legend
plt.legend(handles=[blue_patch, red_patch,green_patch])


# Set plot limits
ax.set_xlim([-limite, limite])
ax.set_ylim([-4, 1])
ax.set_zlim([-1.5, 3])

# Set labels
ax.set_xlabel('V rock')
ax.set_ylabel('V paper')
ax.set_zlabel('V scissors')

mng = plt.get_current_fig_manager()
mng.full_screen_toggle()

# Show plot
plt.show()