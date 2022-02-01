import numpy as np

from breaker_core.model.a_model_linear import AModelLinear

class ModelStatic(AModelLinear):

    def __init__(self, a_x, b_x, a_y, b_y) -> None:
        super().__init__()
        self.matrix_transfrom = np.array(
            [[a_x, 0],
             [0,   a_y],
             [b_x, b_y]])

    def fit(self, matrix_input, matrix_output):
        raise NotImplementedError('This function is not implemented because model is static')
            