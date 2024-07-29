import numpy as np


def min_components(points):
    vectors = np.stack(points) 
    return np.minimum.reduce(vectors)

def max_components(points, infinite_dim_index):
    vectors = np.stack(points) 
    res = np.maximum.reduce(vectors)
    for i in infinite_dim_index:
        res[i] = np.inf
    return res