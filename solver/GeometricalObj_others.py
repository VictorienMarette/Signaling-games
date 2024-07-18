import numpy as np


def min_components(points):
    vectors = np.stack(points) 
    return np.maximum.reduce(vectors)

def max_components(points):
    vectors = np.stack(points) 
    return np.minimum.reduce(vectors)