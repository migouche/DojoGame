import unittest
from dojogame.maths.matrix import Matrix


class MatrixTests(unittest.TestCase):
    def test_matrix_sum(self):
            # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix3 = Matrix([[6, 8], [10, 12]])
        self.assertEqual(matrix1 + matrix2, matrix3)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        matrix3 = Matrix([[11, 13, 15], [17, 19, 21], [23, 25, 27]])
        self.assertEqual(matrix1 + matrix2, matrix3)

    def test_matrix_sub(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix3 = Matrix([[-4, -4], [-4, -4]])
        self.assertEqual(matrix1 - matrix2, matrix3)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        matrix3 = Matrix([[-9, -9, -9], [-9, -9, -9], [-9, -9, -9]])
        self.assertEqual(matrix1 - matrix2, matrix3)

    def test_matrix_neg(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[-1, -2], [-3, -4]])
        self.assertEqual(-matrix1, matrix2)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]])
        self.assertEqual(-matrix1, matrix2)

    def test_matrix_determinant(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        self.assertEqual(matrix1.determinant(), -2)

        # 3x3 matrix
        matrix1 = Matrix([[6, 0, 14], [8, 7, 15], [7, 2, 15]])
        self.assertEqual(matrix1.determinant(), -12)

        # 4x4 matrix
        matrix1 = Matrix([[12, 14, 11, 10], [9, 6, 10, 4], [4, 3, 6, 15], [2, 9, 7, 3]])
        self.assertEqual(matrix1.determinant(), 5782)

    def test_matrix_mul(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix3 = Matrix([[19, 22], [43, 50]])
        self.assertEqual(matrix1 * matrix2, matrix3)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        matrix3 = Matrix([[84, 90, 96], [201, 216, 231], [318, 342, 366]])
        self.assertEqual(matrix1 * matrix2, matrix3)

        # 2x2 matrix * 2x1 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5], [6]])
        matrix3 = Matrix([[17], [39]])
        self.assertEqual(matrix1 * matrix2, matrix3)

        # 3x2 matrix * 2x1 matrix
        matrix1 = Matrix([[1, 2], [3, 4], [5, 6]])
        matrix2 = Matrix([[7], [8]])
        matrix3 = Matrix([[23], [53], [83]])
        self.assertEqual(matrix1 * matrix2, matrix3)

    def test_matrix_transposed(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[1, 3], [2, 4]])
        self.assertEqual(matrix1.transposed(), matrix2)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        self.assertEqual(matrix1.transposed(), matrix2)

    def test_matrix_adjoint(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[4, -3], [-2, 1]])
        self.assertEqual(matrix1.adjoint(), matrix2)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[-3, 6, -3], [6, -12, 6], [-3, 6, -3]])
        self.assertEqual(matrix1.adjoint(), matrix2)

    def adjoint_transpose_conmutative_property(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        self.assertEqual(matrix1.adjoint().transposed(), matrix1.transposed().adjoint())

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(matrix1.adjoint().transposed(), matrix1.transposed().adjoint())

    def test_matrix_inverse(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[-2, 1], [1.5, -0.5]])
        self.assertEqual(matrix1.inverse(), matrix2)

        # 3x3 matrix
        matrix1 = Matrix([[1, 3, 0], [2, 2, 1], [3, 0, 2]])
        matrix2 = Matrix([[4, -6, 3], [-1, 2, -1], [-6, 9, -4]])
        self.assertEqual(matrix1.inverse(), matrix2)

    def test_matrix_div(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix3 = Matrix([[3, -2], [2, -1]])
        self.assertEqual(matrix1 / matrix2, matrix3)

        # 3x3 matrix
        matrix1 = Matrix([[8, 3, 3], [3, 8, 4], [2, 2, 5]])
        matrix2 = Matrix([[1, 3, 0], [2, 1, 2], [1, 0, 1]])
        matrix3 = Matrix([[5, -12, 27], [-1, 11, -18], [-3, 11, -17]])
        self.assertEqual(matrix1 / matrix2, matrix3)

        # 3x2 matrix / 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4], [2, 2]])
        matrix2 = Matrix([[5, 6], [7, 8]])
        matrix3 = Matrix([[3, -2], [2, -1], [-1, 1]])
        self.assertEqual(matrix1 / matrix2, matrix3)

    def test_power(self):
        # 2x2 matrix
        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[95799031216999, 139620104992450], [209430157488675, 305229188705674]])
        self.assertEqual(matrix1 ** 20, matrix2)

        # 3x3 matrix
        matrix1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix2 = Matrix([[121824, 149688, 177552], [275886, 338985, 402084], [429948, 528282, 626616]])
        self.assertEqual(matrix1 ** 5, matrix2)

        # 4x4 matrix
        matrix1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
        matrix2 = Matrix([[256815303580160, 290820022051840, 324824740523520, 358829458995200],
                          [593363704064512, 671930539557888, 750497375051264, 829064210544640],
                          [929912104548864, 1053041057063936, 1176170009579008, 1299298962094080],
                          [1266460505033216, 1434151574569984, 1601842644106752, 1769533713643520]])
        self.assertEqual(matrix1 ** 10, matrix2)
