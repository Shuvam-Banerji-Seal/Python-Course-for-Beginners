# Creating a vector using a simple list
vector_a = [1, 2, 3]
vector_b = [4, 5, 6]

# for i in range(len(vector_a)):
#     sum_results = vector_a[i] + vector_b[i]

# Vector addition using simple lists
vector_sum = [vector_a[i] + vector_b[i] for i in range(len(vector_a))]
print("Vector addition using simple lists:", vector_sum)

# a = [1,2,3]
# b = [4,5,6]
# a = 1i + 2j + 3k
# b = 4i + 5j + 6k
# a.b = 1*4 + 2*5 + 3*6

# Vector dot product using simple lists
dot_product = sum([vector_a[i] * vector_b[i] for i in range(len(vector_a))])
print("Vector dot product using simple lists:", dot_product)

# However, for more complex operations like matrix multiplication, using simple lists can be inefficient and error-prone.
# For example, matrix multiplication is much more complex and requires nested loops which makes the code hard to read and maintain.


# 2d 
#%%
matrix_a = [[1, 2], [3, 4]]
print("length of matrix_a:", len(matrix_a))
# transpose of a matrix
def transpose(matrix):
    # return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] = matrix[j][i]
    return matrix

print("Transpose of matrix_a:", transpose(matrix_a))
# %%


