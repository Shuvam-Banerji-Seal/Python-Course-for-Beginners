import numpy as np

# Creating a vector using numpy arrays
vector_a = np.array ([1, 2, 3, 8])
vector_b = np.array([4, 5, 6, 7])

# Vector addition using numpy arrays
try:
    vector_sum = vector_a + vector_b
    print("Vector addition using numpy arrays:", vector_sum)
except ValueError as e:
    print("Error in vector addition: uoifhdguihewrigheqtight", e)
# vector_sum = vector_a + vector_b
# print("Vector addition using numpy arrays:", vector_sum)

# Vector dot product using numpy arrays
dot_product = np.dot(vector_a, vector_b)
print("Vector dot product using numpy arrays:", dot_product)
# print("next line")
# Numpy also makes it easy to work with matrices (2D arrays)
matrix_a = np.array([[1, 2], 
                     [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])

# # Matrix multiplication using numpy
# matrix_product = np.matmul(matrix_a, matrix_b)
# print("Matrix multiplication using numpy arrays:\n", matrix_product)


# finding the determinant of a matrix
determinant = np.linalg.det(matrix_a)
print("Determinant of the matrix using numpy:", determinant)
