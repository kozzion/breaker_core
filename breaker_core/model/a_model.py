class AModel(object):

    def __init__(self) -> None:
        super().__init__()


    def fit(self, matrix_input, matrix_output):
        raise NotImplementedError('Abstract class')
            
    def transform(self, matrix_input):
        raise NotImplementedError('Abstract class')

    def fit_transform(self, matrix_input, matrix_output):
        self.fit(matrix_input, matrix_output)
        return self.transform(matrix_input)