import numpy as np

from breaker_core.model.a_model_linear import AModelLinear

class ModelStatic(AModelLinear):

    def __init__(self, x_x, x_y, x_o, y_x, y_y, y_o) -> None:
        super().__init__()
        self.matrix_transform = np.array(
            [[x_x, y_x],
             [x_y, y_y],
             [x_o, y_o]])

    @staticmethod
    def from_array(matrix_transform):
        return ModelStatic(
            matrix_transform[0, 0], matrix_transform[1, 0], matrix_transform[2, 0], 
            matrix_transform[0, 1], matrix_transform[1, 1], matrix_transform[2, 1] )


    def fit(self, matrix_input, matrix_output):
        raise NotImplementedError('This function is not implemented because model is static')
            