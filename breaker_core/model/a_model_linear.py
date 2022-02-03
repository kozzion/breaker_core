import numpy as np

from breaker_core.model.a_model import AModel

class AModelLinear(AModel):

    def __init__(self) -> None:
        super().__init__()
        self.matrix_transform = None

    def fit(self, matrix_input, matrix_output_true):
        raise NotImplementedError('Abstract class')
        
    def transform(self, matrix_input):
        if self.matrix_transform is None:
            raise Exception()
        matrix_input = np.c_[ matrix_input, np.ones(matrix_input.shape[0]) ]
        return np.matmul(matrix_input, self.matrix_transform)
