# # Understanding Try and Except in Python

# # For more resources and examples, you can refer to:
# #https://docs.python.org/3/library/exceptions.html

def divide(a, b):
    while True:
        try:
            result = a / b
            return result
        except ValueError:
            print("Error: Invalid input. Please enter valid numbers.")
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed. Please enter a non-zero denominator.")
            b = int(input("Enter the second number (non-zero): "))
        except Exception as eroor:
            print(f"An unexpected error occurred: {eroor}")
            break

# # typeError
# # ValueError
# # IndexError
# # KeyError
# # AttributeError
# # IOError
# # ImportError
# # OverflowError
# # NameError
# # SyntaxError
# # UnboundLocalError
# # IndentationError
# # TypeError
# # FileNotFoundError
# # EOFError
# # AssertionError
# # ImportError
# # UnicodeDecodeError


# # let's explore typeError
# def add_numbers(a, b):
#     while True:
#         try:
#             result = a + b
#             return result
#         except TypeError:
#             print("Error: Invalid input types. Please enter numbers.")
#             a = int(input("Enter the first number: "))
#             b = int(input("Enter the second number: "))
# # let's explore ValueError
# def subtract_numbers(a, b):
#     while True:
#         try:
#             result = a - b
#             return result
#         except ValueError:
#             print("Error: Invalid input. Please enter valid numbers.")
#             a = int(input("Enter the first number: "))
#             b = int(input("Enter the second number: "))
# # let's explore IndexError
# def access_list_element(my_list, index):
#     while True:
#         try:
#             element = my_list[index]
#             return element
#         except IndexError:
#             print("Error: Index out of range. Please enter a valid index.")
#             index = int(input("Enter the index: "))
# # let's explore KeyError
# def access_dict_value(my_dict, key):
#     while True:
#         try:
#             value = my_dict[key]
#             return value
#         except KeyError:
#             print("Error: Key not found. Please enter a valid key.")
#             key = input("Enter the key: ")


def main():
    while True:
        try:
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))
            print("Division:", divide(a, b))
            break
        except ValueError:
            print("Error: Invalid input. Please enter valid numbers.")
        except ZeroDivisionError:
            print("Error: Division by zero is not allowed. Please enter a non-zero denominator.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


#     print("Addition:", add_numbers(a, b))
#     print("Subtraction:", subtract_numbers(a, b))
#     my_list = [1, 2, 3]
#     index = int(input("Enter the index: "))
#     print("Accessing element:", access_list_element(my_list, index))
#     my_dict = {"a": 1, "b": 2, "c": 3}
#     key = input("Enter the key: ")
#     print("Accessing value:", access_dict_value(my_dict, key))
        
if __name__ == "__main__":
    main()


# # handler_statement.py

# # try:
# #     first = float(input("What is your first number? "))
# #     second = float(input("What is your second number? "))
# #     print(f"{first} divided by {second} is {first / second}")
# # except ValueError:
# #     print("You must enter a number")
# # except ZeroDivisionError:
# #     print("You can't divide by zero")


# def divide():
#     while True:
#         try:
#             # Get input first, then handle conversions inside try block
#             a_input = input("Enter the first number: ")
#             b_input = input("Enter the second number: ")
            
#             # Convert to numbers - this can raise ValueError
#             a = float(a_input)
#             b = float(b_input)
            
#             # Check for division by zero
#             if b == 0:
#                 print("Error: Division by zero is not allowed. Please enter a non-zero denominator.")
#                 continue
                
#             # Perform division and return result
#             result = a / b
#             return result
            
#         except ValueError:
#             print("Error: Invalid input. Please enter valid numbers.")
#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
#             return None

# # Example usage
# def main():
#     result = divide()
#     if result is not None:
#         print(f"Result: {result}")
#     else:
#         print("Division operation failed.")

# if __name__ == "__main__":
#     main()