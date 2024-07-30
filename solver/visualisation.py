import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import itertools

def get_all_subsets(lst):
    subsets = []
    for i in range(len(lst) + 1):
        subsets.extend(itertools.combinations(lst, i))
    return subsets


def get_two_matrix(indexs,marge =2):
    infinite_point = np.zeros(3)
    for i in indexs:
        infinite_point[i] = marge
    return infinite_point


def show_BasicConvexeShape3D(ax, shape, points, color):
    vertices = [np.array(points[i]) for i in shape.points_indexs]
    if shape.infinite_hyperplan:
        if len(shape.points_indexs) > 1:
            vertices.append(points[shape.points_indexs[1]] + get_two_matrix([shape.infinite_dim_index[0]]))
        vertices.append(points[shape.points_indexs[0]] + + get_two_matrix([shape.infinite_dim_index[0]]))
        
        if len(shape.infinite_dim_index) > 1:
            if len(shape.points_indexs) > 1:
                vertices.append(points[shape.points_indexs[1]] + get_two_matrix(shape.infinite_dim_index))
            vertices.append(points[shape.points_indexs[0]] + + get_two_matrix(shape.infinite_dim_index))

            vertices.append(points[shape.points_indexs[0]] + + get_two_matrix([shape.infinite_dim_index[1]]))
            if len(shape.points_indexs) > 1:
                vertices.append(points[shape.points_indexs[1]] + get_two_matrix([shape.infinite_dim_index[1]]))

    if len(vertices) == 1:
        ax.scatter(np.array(vertices).T[0], np.array(vertices).T[1], np.array(vertices).T[2], color=color)
    elif len(vertices) == 2:
        ax.plot(np.array(vertices).T[0], np.array(vertices).T[1], np.array(vertices).T[2], linewidth=3, alpha=0.5, color=color)
    else:
        poly = Poly3DCollection([np.array(vertices)], alpha=0.5, color=color)  # Fix: wrap vertices in a list
        ax.add_collection3d(poly)


def show_InterimPayoffPolygone(ax, interimPayoffPolygone, color):
    for basicConvexeShape in interimPayoffPolygone.BasicConvexeShape_array:
        show_BasicConvexeShape3D(ax,basicConvexeShape,interimPayoffPolygone.points, color)


def show_all_InterimPayoffPolygone(InterimPayoffPolygone_array):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['red', 'blue', 'green', 'orange', 'purple']
    i = 0
    for interimPayoffPolygone in InterimPayoffPolygone_array.values():
        show_InterimPayoffPolygone(ax, interimPayoffPolygone, colors[i])
        i += 1

    plt.show()
