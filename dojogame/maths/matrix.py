# dojomaths/matrix.py

from numba import typed


class Matrix:
    def __init__(self, matrix, copy=True):
        # self.matrix = matrix
        self.matrix = matrix
        self.rows = len(self.matrix)

        self.columns = 0 if self.rows == 0 else len(self.matrix[0])
        for row in self.matrix:
            if len(row) != self.columns:
                raise TypeError("Matrix must be rectangular")

        self.dimension = (self.rows, self.columns)

    def to_typed_list(self) -> typed.List:
        m = typed.List()
        for row in self.matrix:
            m.append(typed.List(row))
        return m

    @staticmethod
    def from_typed_list(m: typed.List) -> 'Matrix':
        matrix = []
        for row in m:
            matrix.append(list(row))
        return Matrix(matrix)

    def __getitem__(self, key: int | tuple) -> float | list:
        if isinstance(key, int):
            return self.matrix[key]
        elif isinstance(key, tuple):
            return self.matrix[key[0]][key[1]]
        else:
            raise TypeError("Key must be int or tuple")

    def __setitem__(self, key: int | tuple, value: int | float):
        if isinstance(key, int):
            self.matrix[key] = value
        elif isinstance(key, tuple):
            self.matrix[key[0]][key[1]] = value
        else:
            raise TypeError("Key must be int or tuple")

    def get_element(self, row, column) -> float | int:
        return self.matrix[row][column]

    def get_row(self, row):
        return self.matrix[row]

    def get_column(self, column):
        return [row[column] for row in self.matrix]

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.dimension != other.dimension:
            raise TypeError("Matrices must have the same dimension")
        #return Matrix.from_typed_list(JITMatrix.add(self.to_typed_list(), other.to_typed_list()))
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

    def __mul__(self, other: 'int | float | Matrix') -> 'Matrix':
        if isinstance(other, (int, float)):
            return Matrix([[self.get_element(i, j) * other
                            for j in range(self.columns)] for i in range(self.rows)])
        elif isinstance(other, Matrix):
            if self.columns != other.rows:
                raise TypeError("Matrix dimensions must agree")
            return Matrix([[sum(self.get_element(i, k) * other.get_element(k, j)
                                for k in range(self.columns))
                            for j in range(other.columns)] for i in range(self.rows)])
        else:
            raise TypeError("Can only multiply matrix by int, float or matrix")

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

    def __truediv__(self, other: 'int | float | Matrix'):
        if isinstance(other, (int, float)):
            return self * (1 / other)
        elif isinstance(other, Matrix):
            return self * other.inverse()

    def __eq__(self, other: 'Matrix') -> bool:
        if not isinstance(other, Matrix):
            raise TypeError("Can only compare matrices and entered type is "
                            + str(type(other)) + str(other))
        if self.dimension != other.dimension:
            return False
        for i in range(self.rows):
            for j in range(self.columns):
                if self.get_element(i, j) != other.get_element(i, j):
                    return False
        return True

    def __ne__(self, other: 'Matrix') -> bool:
        return not self.__eq__(other)

    def __str__(self):
        return str(row + "\n" for row in self.matrix)

    def __repr__(self):  # TODO: beautify
        return str(self.matrix)

    def __hash__(self):
        return hash(str(self.matrix))

    @staticmethod
    def parity(r, c):
        return (-1) ** (r + c)

    def remove_row(self, r):
        return Matrix(self.matrix[:r] + self.matrix[r + 1:])

    def remove_column(self, c):
        return self.transposed().remove_row(c).transposed()

    def add_row(self, r: list):
        return Matrix(self.matrix + [r])

    def add_column(self, c: list):
        return self.transposed().add_row(c).transposed()

    def augmented(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows:
            raise TypeError("Matrices must have the same number of rows")
        return Matrix([self.get_row(i) + other.get_row(i) for i in range(self.rows)])

    def determinant(self) -> float | int:
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        if self.rows == 2:
            return self.get_element(0, 0) * self.get_element(1, 1) - \
                self.get_element(0, 1) * self.get_element(1, 0)
        else:
            det = 0
            for i in range(self.columns):
                det += self.get_element(0, i) * Matrix.parity(0, i) * \
                       self.remove_row(0).remove_column(i).determinant()

            return det

    def transposed(self) -> 'Matrix':
        return Matrix(list(map(list, zip(*self.matrix))))

    def adjoint(self) -> 'Matrix':
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        if self.rows == 2:
            return Matrix([[self.get_element(1, 1), -self.get_element(1, 0)],
                           [-self.get_element(0, 1), self.get_element(0, 0)]])
        else:
            return Matrix([[Matrix.parity(i, j) * self.remove_row(i).remove_column(j).determinant()
                            for j in range(self.columns)] for i in range(self.rows)])

    def inverse(self) -> 'Matrix':
        if self.rows != self.columns:
            raise TypeError("Matrix must be square")
        det = self.determinant()

        if det == 0:
            raise ZeroDivisionError("Matrix is singular")
        return self.adjoint().transposed() / det

    @staticmethod
    def from_row_matrix(row_matrix: 'list | Matrix') -> 'Matrix':
        if isinstance(row_matrix, Matrix):
            return row_matrix.transposed()
        return Matrix(row_matrix).transposed()

    @staticmethod
    def empty(rows, columns):
        return Matrix([[0] * columns] * rows)
