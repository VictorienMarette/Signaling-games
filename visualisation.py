import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch

# Create a figure and a 3D axis
limite = 6

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def plotwithtrans(x,y,z, color):
    # point et droite
    ax.scatter([3+x,-3+x], [-3+y,0+y], [0+z,3+z], color=color)
    ax.plot(np.array([3+x,-3+x]), np.array([-3+y,0+y]), np.array([0+z,3+z]), alpha=0.5, color=color)

    #plan 1
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [-3+x, 0+y, 3+z], # Point B
        [-3+x, 0+y, 1.5*limite],# Point C
        [3+x, -3+y, 1.5*limite]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 2
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [-3+x, 0+y, 3+z], # Point B
        [-3+x, 1.5*limite, 3+z],# Point C
        [3+x, 1.5*limite, 0+z]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 3
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [1.5*limite, -3+y, 0+z], # Point B
        [1.5*limite, 1.5*limite, 0+z],# Point C
        [3+x, 1.5*limite, 0+z]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 4
    points = np.array([
        [3+x, -3+y, 0+z],  # Point A
        [1.5*limite, -3+y, 0+z], # Point B
        [1.5*limite, -3+y, 1.5*limite],# Point C
        [3+x, -3+y, 1.5*limite]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor=color, edgecolor=color)
    ax.add_collection3d(poly)

    #plan 5
    points = np.array([
        [-3+x, 0+y, 3+z],  # Point A
        [-3+x, 0+y, 1.5*limite], # Point B
        [-3+x, 1.5*limite, 1.5*limite],# Point C
        [-3+x, 1.5*limite, 3+z]  # Point D
    ])
    x1, y1, z1 = points[:, 0], points[:, 1], points[:, 2]
    vertices = [list(zip(x1, y1, z1))]
    poly = Poly3DCollection(vertices, alpha=0.5, facecolor='b', edgecolor=color)
    ax.add_collection3d(poly)

#E pour le signal Rock s translation de (0,-1,-2)
plotwithtrans(0,-1,-2, "b")

#E pour le signal Paper s translation de (-2,0,-1)
plotwithtrans(-2,0,-1, "r")

origin = [0, 0, 0]
ax.quiver(*origin, 2, 0, 0, color='red', arrow_length_ratio=0.1, label='X axis')
ax.quiver(*origin, 0, 2, 0, color='green', arrow_length_ratio=0.1, label='Y axis')
ax.quiver(*origin, 0, 0, 2, color='blue', arrow_length_ratio=0.1, label='Z axis')


# Define custom legend patches
blue_patch = Patch(color='blue', label=r'$\mathcal{E}(Rock \ s,.)$')
red_patch = Patch(color='red', label=r'$\mathcal{E}(Paper \ s,.)$')

# Add the custom legend
plt.legend(handles=[blue_patch, red_patch])


# Set plot limits
ax.set_xlim([-limite, limite])
ax.set_ylim([-limite, limite])
ax.set_zlim([-limite, limite])

# Set labels
ax.set_xlabel('V rock')
ax.set_ylabel('V paper')
ax.set_zlabel('V scissors')

# Show plot
plt.show()