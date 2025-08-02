import numpy as np
import time


# check the time for running the code

def determinant(matrix):
    return np.linalg.det(matrix)


def determinant_recursive(matrix):
    n = len(matrix)

    #Base case for 1x1 matrix
    if n == 1:
        return matrix[0][0]
    #Base case for 2x2 matrix
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    determinant = 0

    for j in range(n):
        # Cal the cofactor of the first row
        cofactor = (-1)**j * matrix[0][j] * determinant_recursive(get_minor(matrix, 0, j))
        determinant += cofactor
    return determinant





def get_minor(matrix, row, col):
   # for row in (matrix[:row] + matrix[row+1:]):
   #     yield row[:col] + row[col+1:]
    return [row[:col] + row[col+1:] for row in (matrix[:row] + matrix[row+1:])]

matrix = [[1, 4, 2, 3], [0, 1, 4, 4], [-1, 0, 4, 4], [2, 0, 4, 1]]
start_time = time.time()
print("Determinant using numpy:", determinant(matrix))
print("Time taken using numpy:", time.time() - start_time)

start_time = time.time()
print("Determinant using recursive function:", determinant_recursive(matrix))
print("Time taken using recursive function:", time.time() - start_time)