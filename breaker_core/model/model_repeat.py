import numpy as np

from breaker_core.model.a_model import AModel

class ModelRepeat(AModel):

    def __init__(self, 
            model_0:AModel, 
            model_1:AModel, 
            fraction_select:float = 0.5, 
            count_reselect:int = 1) -> None:    

        super().__init__()
        self.model_0 = model_0
        self.model_1 = model_1
        self.fraction_select = fraction_select
        self.count_reselect = count_reselect

    def compute_error_euclidian(self, matrix_output_pred, matrix_output_true):
        array_dif = matrix_output_pred - matrix_output_true
        array_dif2 = np.multiply(array_dif, array_dif)
        return np.sqrt(array_dif2[:, 0] + array_dif2[:, 1])

    def select(self, matrix_input, matrix_output_true):
        matrix_input_pred = self.model_0.transform(matrix_input)
        array_error = self.compute_error_euclidian(matrix_input_pred, matrix_output_true)
        limit_selection = np.quantile(array_error, self.fraction_select)
        array_selection = array_error < limit_selection
        return array_selection

    def fit(self, matrix_input, matrix_output_true):
        for _ in range(self.count_reselect):
            self.model_0.fit(matrix_input, matrix_output_true)
            array_selection = self.select(matrix_input, matrix_output_true)
        self.model_1.fit(matrix_input[array_selection, :], matrix_output_true[array_selection, :])

    def transform(self, matrix_input):
        return self.model_1.transform(matrix_input)
