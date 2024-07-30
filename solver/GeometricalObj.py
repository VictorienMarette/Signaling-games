import numpy as np

from GeometricalObj_others import *

class BasicConvexeShape:

    def __init__(self, points_indexs, points, infinite_dim_index):
        self.points_indexs = points_indexs
        self.infinite_dim_index = infinite_dim_index
        self.len_T = points[0].size
        self.bording_box_low = min_components(points)
        self.bording_box_high = max_components(points,infinite_dim_index)
        self.infinite_hyperplan = not len(infinite_dim_index) == 0


class InterimPayoffPolygone:

    def __init__(self, points, indifferent_actions_beliefs):
        self.points = points

        self.BasicConvexeShape_array = []
        for actions in indifferent_actions_beliefs.keys():
            for infinite_dim_index in indifferent_actions_beliefs[actions]:
                self.BasicConvexeShape_array.append(BasicConvexeShape(actions, points, infinite_dim_index))

        intir = self.calculate_intir()


    def calculate_intir(self):
        return None