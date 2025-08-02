# Matrix Multiplication: Detailed Explanation and Implementation

## Introduction to Matrix Multiplication

#Matrix multiplication is a fundamental operation in linear algebra that allows us to multiply two matrices together. There are several ways to implement matrix multiplication in Python:

# 1. Nested loop method (manual implementation)
# 2. NumPy method (optimized library implementation)
# 3. Mathematical definition method

#Let's explore each of these approaches:

## 1. Manual Matrix Multiplication Using Nested Loops

def manual_matrix_multiply(A, B):
    """
    Manually multiply two matrices using nested loops.
    
    Parameters:
    A (list of lists): First input matrix
    B (list of lists): Second input matrix
    
    Returns:
    list of lists: Resulting matrix after multiplication
    """
    # Check if multiplication is possible
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in first matrix must equal number of rows in second matrix")
    
    # Initialize result matrix with zeros
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    
    # Perform matrix multiplication
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

## Example Usage of Manual Method
A = [
    [1, 2],
    [3, 4]
]

B = [
    [5, 6],
    [7, 8]
]

print("Matrix A:")
for row in A:
    print(row)

print("\nMatrix B:")
for row in B:
    print(row)

print("\nManual Matrix Multiplication Result:")
result = manual_matrix_multiply(A, B)
for row in result:
    print(row)

## 2. NumPy Matrix Multiplication

import numpy as np

def numpy_matrix_multiply(A, B):
    """
    Perform matrix multiplication using NumPy.
    
    Parameters:
    A (array-like): First input matrix
    B (array-like): Second input matrix
    
    Returns:
    numpy.ndarray: Resulting matrix after multiplication
    """
    return np.dot(A, B)

## NumPy Example
numpy_A = np.array(A)
numpy_B = np.array(B)

print("\nNumPy Matrix Multiplication Result:")
numpy_result = numpy_matrix_multiply(numpy_A, numpy_B)
print(numpy_result)

## 3. Mathematical Definition Method

def math_matrix_multiply(A, B):
    """
    Implement matrix multiplication using list comprehension 
    based on mathematical definition.
    
    Parameters:
    A (list of lists): First input matrix
    B (list of lists): Second input matrix
    
    Returns:
    list of lists: Resulting matrix after multiplication
    """
    # Check matrix multiplication compatibility
    if len(A[0]) != len(B):
        raise ValueError("Invalid matrix dimensions")
    
    # Use list comprehension to calculate each element
    return [
        [sum(a * b for a, b in zip(row, col)) for col in zip(*B)]
        for row in A
    ]

## Example with Different Sized Matrices
C = [
    [1, 2, 3],
    [4, 5, 6]
]

D = [
    [7, 8],
    [9, 10],
    [11, 12]
]

print("\nMath Method Matrix Multiplication:")
math_result = math_matrix_multiply(C, D)
for row in math_result:
    print(row)

## Performance Comparison
import timeit

# Timing manual method
manual_time = timeit.timeit(
    lambda: manual_matrix_multiply(A, B), 
    number=10000
)

# Timing NumPy method
numpy_time = timeit.timeit(
    lambda: numpy_matrix_multiply(numpy_A, numpy_B), 
    number=10000
)

print("\nPerformance Comparison:")
print(f"Manual Method Time: {manual_time:.6f} seconds")
print(f"NumPy Method Time: {numpy_time:.6f} seconds")

## Key Takeaways
# 1. Manual method is intuitive but slow for large matrices
# 2. NumPy is highly optimized and much faster
# 3. Mathematical method is concise but may have performance limitations