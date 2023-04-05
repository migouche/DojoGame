from dojogame.maths.matrix import Matrix
from numba import typed, typeof

m: typed.List = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).to_typed_list()
print(len(m[1]))

mat = Matrix.from_typed_list(m)
print(mat.matrix)



