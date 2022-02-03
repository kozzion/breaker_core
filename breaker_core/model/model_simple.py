import numpy as np


from breaker_core.model.a_model_linear import AModelLinear


class ModelSimple(AModelLinear):

    def __init__(self) -> None:
        super().__init__()

    def fit(self, matrix_input, matrix_output):
        count_dim = matrix_input.shape[1] 
        if matrix_input.shape[1] != matrix_output.shape[1]:
            raise Exception()
        matrix_input = np.c_[ matrix_input, np.ones(matrix_input.shape[0]) ]

        self.matrix_transform = np.zeros((count_dim + 1, count_dim))
        for i in range(count_dim):
            array_input= matrix_input[:,i]
            array_output = matrix_output[:,i]
            range_input = np.max(array_input) - np.min(array_input)
            range_output = np.max(array_output) - np.min(array_output)
            factor = range_output / range_input
            if np.corrcoef([array_input, array_output])[0, 1] < 0:
                factor *= -1 # flip for negative correlation 
            difference = np.min(array_output) - np.min(array_input * factor)
            self.matrix_transform[i, i] = factor
            self.matrix_transform[count_dim, i] = difference
            