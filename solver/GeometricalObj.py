import numpy as np

from GeometricalObj_others import *

class BasicConvexeShape:

    def __init__(self, points_indexs, points):
        points_indexs = points_indexs
        bording_box_low = min_components(points)
        bording_box_low = max_components(points)