# Step 1: Introduction to Vectors and Matrices
import re


print("Step 1: Introduction to Vectors and Matrices")
print("A vector is a one-dimensional array of numbers.")
print("A matrix is a two-dimensional array of numbers arranged in rows and columns.")
print("")

#%%
# Step 2: Basic Vector Operations Using Python Lists
print("Step 2: Basic Vector Operations Using Python Lists")
vector_a = [1, 2, 3]
vector_b = [4, 5, 6]

# Vector addition using simple lists
vector_sum = [vector_a[i] + vector_b[i] for i in range(len(vector_a))]
print("Vector addition (using simple lists):", vector_sum)

# Vector subtraction using simple lists
vector_diff = [vector_a[i] - vector_b[i] for i in range(len(vector_a))]
print("Vector subtraction (using simple lists):", vector_diff)

#%%
# Scalar multiplication of a vector using simple lists
scalar = 2
scaled_vector = [scalar * i for i in vector_a]
print("Scalar multiplication (using simple lists):", scaled_vector)

#%%
# Dot product of two vectors using simple lists
dot_product = sum([vector_a[i] * vector_b[i] for i in range(len(vector_a))])
print("Dot product (using simple lists):", dot_product)
print("")

#%%
# Step 3: Basic Matrix Operations Using Python Nested Lists
print("Step 3: Basic Matrix Operations Using Python Nested Lists")
matrix_a = [[1, 2], [3, 4]]
matrix_b = [[5, 6], [7, 8]]

# Matrix addition using nested lists
matrix_sum = [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
# understanding the above line:
# - For each row i in matrix_a, we create a new row by adding corresponding elements from matrix_a and matrix_b.    
# for i in range(len(matrix_a)):
#     for j in range(len(matrix_a[0])):
#         matrix_sum[i][j] = matrix_a[i][j] + matrix_b[i][j]
#         print(f"Adding {matrix_a[i][j]} and {matrix_b[i][j]} to get {matrix_sum[i][j]}")
print("Matrix addition (using nested lists):", matrix_sum)

# Matrix subtraction using nested lists
matrix_diff = [[matrix_a[i][j] - matrix_b[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
print("Matrix subtraction (using nested lists):", matrix_diff)

# Scalar multiplication of a matrix using nested lists
scalar = 2
scaled_matrix = [[scalar * matrix_a[i][j] for j in range(len(matrix_a[0]))] for i in range(len(matrix_a))]
print("Scalar multiplication for a matrix (using nested lists):", scaled_matrix)

# Matrix multiplication using nested lists
def matrix_mul(A, B):
    """
    Multiply two matrices A and B.
    
    Parameters
    ----------
    A : list of lists
        First matrix
    B : list of lists
        Second matrix
    
    Returns
    -------
    list of lists
        Resulting matrix after multiplication
    """
    
    result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
    return result

# expanding the zip:
# Base idea of matrix multiplication
#%%
result = [[0 for _ in range(len(matrix_b[0]))] for _ in range(len(matrix_a))]
import pprint
pprint.pp (result)
for i in range(len(matrix_a)):
    for j in range(len(matrix_b[0])):
        for k in range(len(matrix_b)):
            result[i][j] += matrix_a[i][k] * matrix_b[k][j]

print("Matrix multiplication (using nested lists):", result)

#%%
matrix_product = matrix_mul(matrix_a, matrix_b)
print("Matrix multiplication (using nested lists):", matrix_product)
print("")

# Step 4: Introduction to NumPy
print("Step 4: Introduction to NumPy")
print("NumPy is a powerful library for numerical computations in Python. It provides a high-performance multidimensional array object and tools for working with these arrays.")
print("NumPy makes operations on vectors and matrices much easier and more efficient.")
print("")

# Step 5: Vector Operations Using NumPy
import numpy as np
print("Step 5: Vector Operations Using NumPy")
vector_a = np.array([1, 2, 3])
vector_b = np.array([4, 5, 6])

# Vector addition using NumPy
vector_sum = vector_a + vector_b
print("Vector addition (using NumPy):", vector_sum)

# Vector subtraction using NumPy
vector_diff = vector_a - vector_b
print("Vector subtraction (using NumPy):", vector_diff)

# Scalar multiplication of a vector using NumPy
scaled_vector = 2 * vector_a
print("Scalar multiplication (using NumPy):", scaled_vector)

# Dot product of two vectors using NumPy
dot_product = np.dot(vector_a, vector_b)
print("Dot product (using NumPy):", dot_product)
print("")

# Step 6: Matrix Operations Using NumPy
print("Step 6: Matrix Operations Using NumPy")
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])

# Matrix addition using NumPy
matrix_sum = matrix_a + matrix_b
print("Matrix addition (using NumPy):\n", matrix_sum)

# Matrix subtraction using NumPy
matrix_diff = matrix_a - matrix_b
print("Matrix subtraction (using NumPy):\n", matrix_diff)

# Scalar multiplication of a matrix using NumPy
scaled_matrix = 2 * matrix_a
print("Scalar multiplication for a matrix (using NumPy):\n", scaled_matrix)

# Matrix multiplication using NumPy
matrix_product = np.matmul(matrix_a, matrix_b)
print("Matrix multiplication (using NumPy):\n", matrix_product)
print("")

# Step 7: Advanced Matrix Operations Using NumPy
print("Step 7: Advanced Matrix Operations Using NumPy")
matrix = np.array([[1, 2], [3, 4]])

# Transpose of a matrix using NumPy
matrix_transpose = matrix.T
print("Transpose of the matrix (using NumPy):\n", matrix_transpose)

# Inverse of a matrix using NumPy
try:
    matrix_inverse = np.linalg.inv(matrix)
    print("Inverse of the matrix (using NumPy):\n", matrix_inverse)
except np.linalg.LinAlgError:
    print("The matrix is not invertible.")

# Determinant of a matrix using NumPy
matrix_det = np.linalg.det(matrix)
print("Determinant of the matrix (using NumPy):", matrix_det)

# Eigenvalues and eigenvectors of a matrix using NumPy
eigenvalues, eigenvectors = np.linalg.eig(matrix)
print("Eigenvalues of the matrix (using NumPy):", eigenvalues)
print("Eigenvectors of the matrix (using NumPy):\n", eigenvectors)
print("")

# Step 8: Conclusion and Additional Resources
print("Step 8: Conclusion and Additional Resources")
print("In this course, we covered basic and advanced operations on vectors and matrices using both standard Python lists and the NumPy library. NumPy provides a more efficient and convenient way to handle these operations.")
print("For further learning, you can check out the NumPy documentation and other online resources on linear algebra in Python.")
