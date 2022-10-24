# dojomaths/matrix.py


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(self.matrix)
        self.columns = len(self.matrix[0])
        for row in self.matrix:
            if len(row) != self.columns:
                raise TypeError("Matrix must be rectangular")

        self.dimension = (self.rows, self.columns)

    def __getitem__(self, key: int | tuple) -> float | list:
        if isinstance(key, int):
            return self.matrix[key]
        elif isinstance(key, tuple):
            return self.matrix[key[0]][key[1]]
        else:
            raise TypeError("Key must be int or tuple")

    def get_element(self, row, column):
        return self.matrix[row][column]

    def get_row(self, row):
        return self.matrix[row]

    def get_column(self, column):
        return [row[column] for row in self.matrix]

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.dimension != other.dimension:
            raise TypeError("Matrices must have the same dimension")
        return Matrix([[self.matrix[i][j] + other.matrix[i][j]
                        for j in range(self.columns)] for i in range(self.rows)])

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        if self.dimension != other.dimension:
            raise TypeError("Matrices must have the same dimension")
        return Matrix([[self.matrix[i][j] - other.matrix[i][j]
                        for j in range(self.columns)] for i in range(self.rows)])

    def __neg__(self):
        return Matrix([[-self.matrix[i][j]
                        for j in range(self.columns)] for i in range(self.rows)])

    def __mul__(self, other: int | float):
        return Matrix([[self.matrix[i][j] * other
                        for j in range(self.columns)] for i in range(self.rows)])

    def __pow__(self, power):
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        if power == 0:
            return Matrix([[int(i == j) for j in range(self.columns)] for i in range(self.rows)])
        elif power == 1:
            return self
        elif power < 0:
            return self.inverse() ** (-power)
        else:
            return self * (self ** (power - 1))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other: int | float | 'Matrix'):

        return Matrix([[self.matrix[i][j] / other
                        for j in range(self.columns)] for i in range(self.rows)])

    def __eq__(self, other: 'Matrix') -> bool:
        if self.dimension != other.dimension:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True

    def __ne__(self, other: 'Matrix') -> bool:
        return not self == other

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):  # TODO: beautify
        return str(self.matrix)

    def __hash__(self):
        return hash(str(self.matrix))

    def determinant(self) -> float | int:
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        if self.rows == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        else:
            det = 0
            for i in range(self.rows):
                det += (-1) ** i * self.matrix[0][i] * \
                       Matrix([row[:i] + row[i + 1:]
                               for row in self.matrix[1:]]).determinant()
            return det

    def transposed(self) -> 'Matrix':
        return Matrix([[self.matrix[j][i] for j in range(self.rows)] for i in range(self.columns)])

    def adjugate(self) -> 'Matrix':
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        return Matrix([[(-1) ** (i + j) * Matrix(
            [row[:j] + row[j + 1:] for row in self.matrix[:i] + self.matrix[i + 1:]]).determinant()
                        for j in range(self.columns)] for i in range(self.rows)])

    def inverse(self) -> 'Matrix':
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        det = self.determinant()
        if det == 0:
            raise ZeroDivisionError("Matrix is singular")
        return (1 / det) * self.adjugate().transposed()

    @staticmethod
    def from_row_matrix(row_matrix: list | 'Matrix') -> 'Matrix':
        if isinstance(row_matrix, Matrix):
            return row_matrix.transposed()
        return Matrix(row_matrix).transposed()
