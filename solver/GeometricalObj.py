import numpy as np

from GeometricalObj_others import *

class BasicConvexeShape:

    def __init__(self, points_indexs, points, infinite_dim_index):
        points_indexs = points_indexs
        infinite_dim_index = infinite_dim_index
        len_T = points[0].size
        bording_box_low = min_components(points)
        bording_box_high = max_components(points,infinite_dim_index)


class InterimPayoffPolygone:

    def __init__(self, points, indifferent_actions_beliefs):
        BasicConvexeShape_array = []
        for actions in indifferent_actions_beliefs.keys():
            for infinite_dim_index in indifferent_actions_beliefs[actions]:
                BasicConvexeShape_array.append(BasicConvexeShape(actions, points, infinite_dim_index))

        intir = self.calculate_intir()


    def calculate_intir(self):
        return None