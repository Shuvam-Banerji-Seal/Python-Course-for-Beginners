# Advanced Matrix Manipulation Problems

import numpy as np
from typing import List, Tuple, Optional

class MatrixManipulator:
    @staticmethod
    def matrix_spiral_traversal(matrix: List[List[int]]) -> List[int]:
        """
        Traverse a matrix in a spiral order from outer layer to inner core.
        
        Time Complexity: O(m*n)
        Space Complexity: O(1) extra space
        """
        if not matrix or not matrix[0]:
            return []
        
        result = []
        rows, cols = len(matrix), len(matrix[0])
        top, bottom, left, right = 0, rows - 1, 0, cols - 1
        
        while top <= bottom and left <= right:
            # Traverse right
            for j in range(left, right + 1):
                result.append(matrix[top][j])
            top += 1
            
            # Traverse down
            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1
            
            if top <= bottom:
                # Traverse left
                for j in range(right, left - 1, -1):
                    result.append(matrix[bottom][j])
                bottom -= 1
            
            if left <= right:
                # Traverse up
                for i in range(bottom, top - 1, -1):
                    result.append(matrix[i][left])
                left += 1
        
        return result

    @staticmethod
    def matrix_rotation(matrix: List[List[int]], clockwise: bool = True) -> List[List[int]]:
        """
        Rotate matrix 90 degrees clockwise or counter-clockwise.
        
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        n = len(matrix)
        
        # Transpose the matrix
        for i in range(n):
            for j in range(i, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        # Reverse rows
        if clockwise:
            for i in range(n):
                matrix[i] = matrix[i][::-1]
        else:
            for i in range(n):
                matrix[i].reverse()
        
        return matrix

    @staticmethod
    def matrix_diagonals_operations(matrix: List[List[int]]) -> Tuple[int, int, float]:
        """
        Perform various diagonal operations:
        1. Primary diagonal sum
        2. Secondary diagonal sum
        3. Average of diagonal elements
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        n = len(matrix)
        primary_diagonal_sum = 0
        secondary_diagonal_sum = 0
        diagonal_elements = []
        
        for i in range(n):
            # Primary diagonal (top-left to bottom-right)
            primary_diagonal_sum += matrix[i][i]
            
            # Secondary diagonal (top-right to bottom-left)
            secondary_diagonal_sum += matrix[i][n - 1 - i]
            
            diagonal_elements.extend([matrix[i][i], matrix[i][n - 1 - i]])
        
        # Remove duplicates for square matrices
        diagonal_elements = list(set(diagonal_elements))
        diagonal_avg = sum(diagonal_elements) / len(diagonal_elements)
        
        return primary_diagonal_sum, secondary_diagonal_sum, diagonal_avg

    @staticmethod
    def submatrix_maximum_sum(matrix: List[List[int]]) -> int:
        """
        Kadane's algorithm for maximum submatrix sum.
        
        Time Complexity: O(n^3)
        Space Complexity: O(n)
        """
        rows, cols = len(matrix), len(matrix[0])
        max_sum = float('-inf')
        
        # Try all possible left and right column combinations
        for left in range(cols):
            temp = [0] * rows
            
            for right in range(left, cols):
                # Add current column to temp
                for i in range(rows):
                    temp[i] += matrix[i][right]
                
                # Apply Kadane's algorithm on temp
                current_sum = 0
                local_max = float('-inf')
                
                for element in temp:
                    current_sum = max(element, current_sum + element)
                    local_max = max(local_max, current_sum)
                
                max_sum = max(max_sum, local_max)
        
        return max_sum

    @staticmethod
    def matrix_snake_pattern_traversal(matrix: List[List[int]]) -> List[int]:
        """
        Traverse matrix in a snake-like pattern (alternating left-right, right-left).
        
        Time Complexity: O(m*n)
        Space Complexity: O(1)
        """
        result = []
        for i in range(len(matrix)):
            # Even rows go left to right
            if i % 2 == 0:
                result.extend(matrix[i])
            # Odd rows go right to left
            else:
                result.extend(matrix[i][::-1])
        
        return result

    @staticmethod
    def find_saddle_points(matrix: List[List[int]]) -> List[Tuple[int, int]]:
        """
        Find saddle points in a matrix (elements that are 
        minimum in their row and maximum in their column).
        
        Time Complexity: O(m*n)
        Space Complexity: O(1)
        """
        rows, cols = len(matrix), len(matrix[0])
        saddle_points = []
        
        for i in range(rows):
            # Find row minimum
            row_min = min(matrix[i])
            row_min_indices = [j for j in range(cols) if matrix[i][j] == row_min]
            
            for col_index in row_min_indices:
                # Check if row minimum is column maximum
                if matrix[i][col_index] == max(matrix[r][col_index] for r in range(rows)):
                    saddle_points.append((i, col_index))
        
        return saddle_points

# Demonstration of Matrix Manipulation Techniques
def demonstrate_matrix_manipulations():
    # Sample matrix for demonstrations
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    manipulator = MatrixManipulator()
    
    # Spiral Traversal
    print("Spiral Traversal:", manipulator.matrix_spiral_traversal(matrix))
    
    # Matrix Rotation
    rotated_matrix = manipulator.matrix_rotation(matrix.copy())
    print("Clockwise Rotated Matrix:", rotated_matrix)
    
    # Diagonal Operations
    primary_sum, secondary_sum, diagonal_avg = manipulator.matrix_diagonals_operations(matrix)
    print(f"Diagonal Sums - Primary: {primary_sum}, Secondary: {secondary_sum}")
    print(f"Diagonal Average: {diagonal_avg}")
    
    # Submatrix Maximum Sum
    max_submatrix_sum = manipulator.submatrix_maximum_sum(matrix)
    print("Maximum Submatrix Sum:", max_submatrix_sum)
    
    # Snake Pattern Traversal
    snake_traversal = manipulator.matrix_snake_pattern_traversal(matrix)
    print("Snake Pattern Traversal:", snake_traversal)
    
    # Saddle Points
    saddle_points = manipulator.find_saddle_points(matrix)
    print("Saddle Points:", saddle_points)

if __name__ == "__main__":
    demonstrate_matrix_manipulations()