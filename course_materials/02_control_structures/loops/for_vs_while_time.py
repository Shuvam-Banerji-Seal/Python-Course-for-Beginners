# let's compare the time between the for loop and the while loop to do sorting of 1 million numbers




# import time

# start_time = time.time()
# factorial = 1
# for i in range(1, 601):
#     factorial *= i
# end_time = time.time()
# print("For loop took", end_time - start_time, "seconds to calculate the factorial of 20.")

# start_time = time.time()
# factorial = 1
# i = 1
# while i <= 600:
#     factorial *= i
#     i += 1
# end_time = time.time()
# print("While loop took", end_time - start_time, "seconds to calculate the factorial of 20.")    

import time
import random
import numpy as np


# Generate a list of 1 million random numbers
def generate_random_numbers(size=1000000):
    return [random.randint(1, 1000000) for _ in range(size)]
# Sort using the built-in sort method
def sort_with_builtin(numbers):
    numbers.sort()
    return numbers
# Sort using the bubble sort algorithm
def sort_with_bubble(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers
# Sort using the selection sort algorithm
def sort_with_selection(numbers):
    n = len(numbers)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if numbers[j] < numbers[min_idx]:
                min_idx = j
        numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]
    return numbers