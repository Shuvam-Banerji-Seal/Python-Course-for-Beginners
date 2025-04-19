# Understanding Try and Except in Python

# For more resources and examples, you can refer to:
#https://docs.python.org/3/library/exceptions.html

def divide(a, b):
    while True:
        try:
            result = a / b
            return result
        except ZeroDivisionError:
            print("Error: Cannot divide by zero. Please enter valid numbers.")
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))


# typeError
# ValueError
# IndexError
# KeyError
# AttributeError
# IOError
# ImportError
# OverflowError
# NameError
# SyntaxError
# UnboundLocalError
# IndentationError
# TypeError
# FileNotFoundError
# EOFError
# AssertionError
# ImportError
# UnicodeDecodeError


# let's explore typeError
def add_numbers(a, b):
    while True:
        try:
            result = a + b
            return result
        except TypeError:
            print("Error: Invalid input types. Please enter numbers.")
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))
# let's explore ValueError
def subtract_numbers(a, b):
    while True:
        try:
            result = a - b
            return result
        except ValueError:
            print("Error: Invalid input. Please enter valid numbers.")
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))
# let's explore IndexError
def access_list_element(my_list, index):
    while True:
        try:
            element = my_list[index]
            return element
        except IndexError:
            print("Error: Index out of range. Please enter a valid index.")
            index = int(input("Enter the index: "))
# let's explore KeyError
def access_dict_value(my_dict, key):
    while True:
        try:
            value = my_dict[key]
            return value
        except KeyError:
            print("Error: Key not found. Please enter a valid key.")
            key = input("Enter the key: ")


def main():
    a = int(input("Enter the first number: "))
    b = int(input("Enter the second number: "))
    print("Addition:", add_numbers(a, b))
    print("Subtraction:", subtract_numbers(a, b))
    my_list = [1, 2, 3]
    index = int(input("Enter the index: "))
    print("Accessing element:", access_list_element(my_list, index))
    my_dict = {"a": 1, "b": 2, "c": 3}
    key = input("Enter the key: ")
    print("Accessing value:", access_dict_value(my_dict, key))
        
if __name__ == "__main__":
    main()