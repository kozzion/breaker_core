
import numpy as np

from breaker_core.model.a_model_linear import AModelLinear

class ModelLeastSquares(AModelLinear):

    def __init__(self) -> None:
        super().__init__()


    def fit(self, matrix_input, matrix_output_true):
        matrix_input = np.c_[ matrix_input, np.ones(matrix_input.shape[0]) ]
        list_array_calibration = []
        for i in range(matrix_output_true.shape[1]):
            array_output = matrix_output_true[:,i]
            array_calibration, error, rank, sing = np.linalg.lstsq(matrix_input, array_output, rcond=None)
            list_array_calibration.append(array_calibration)
        self.matrix_transform = np.vstack(list_array_calibration).transpose()
