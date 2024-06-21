import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Create a figure and a 3D axis
limite = 6

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# point et droite
ax.scatter([3,-3], [-3,0], [0,3], color='b')
ax.plot(np.array([3,-3]), np.array([-3,0]), np.array([0,3]), alpha=0.5, color='b')


#plan 1
points = np.array([
    [3, -3, 0],  # Point A
    [-3, 0, 3], # Point B
    [-3, 0, 1.5*limite],# Point C
    [3, -3, 1.5*limite]  # Point D
])
x, y, z = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x, y, z))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor='b', edgecolor='b')
ax.add_collection3d(poly)

#plan 2
points = np.array([
    [3, -3, 0],  # Point A
    [-3, 0, 3], # Point B
    [-3, 1.5*limite, 3],# Point C
    [3, 1.5*limite, 0]  # Point D
])
x, y, z = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x, y, z))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor='b', edgecolor='b')
ax.add_collection3d(poly)

#plan 3
points = np.array([
    [3, -3, 0],  # Point A
    [1.5*limite, -3, 0], # Point B
    [1.5*limite, 1.5*limite, 0],# Point C
    [3, 1.5*limite, 0]  # Point D
])
x, y, z = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x, y, z))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor='b', edgecolor='b')
ax.add_collection3d(poly)

#plan 4
points = np.array([
    [3, -3, 0],  # Point A
    [1.5*limite, -3, 0], # Point B
    [1.5*limite, -3, 1.5*limite],# Point C
    [3, -3, 1.5*limite]  # Point D
])
x, y, z = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x, y, z))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor='b', edgecolor='b')
ax.add_collection3d(poly)

#plan 5
points = np.array([
    [-3, 0, 3],  # Point A
    [-3, 0, 1.5*limite], # Point B
    [-3, 1.5*limite, 1.5*limite],# Point C
    [-3, 1.5*limite, 3]  # Point D
])
x, y, z = points[:, 0], points[:, 1], points[:, 2]
vertices = [list(zip(x, y, z))]
poly = Poly3DCollection(vertices, alpha=0.5, facecolor='b', edgecolor='b')
ax.add_collection3d(poly)

origin = [0, 0, 0]
ax.quiver(*origin, 2, 0, 0, color='red', arrow_length_ratio=0.1, label='X axis')
ax.quiver(*origin, 0, 2, 0, color='green', arrow_length_ratio=0.1, label='Y axis')
ax.quiver(*origin, 0, 0, 2, color='blue', arrow_length_ratio=0.1, label='Z axis')


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