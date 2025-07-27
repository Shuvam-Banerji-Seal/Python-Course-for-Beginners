import sys


def isArmstrongNumber(num: int) -> bool:
    """ #docstring
    Check if a number is an Armstrong number.
    
    An Armstrong number (or narcissistic number) is a number that is equal to the sum of its own digits raised to the power of the number of digits.
    
    Args:
        num (int): The number to check.
        
    Returns:
        bool: True if num is an Armstrong number, False otherwise.
    """
    # Convert the number to string to easily iterate over digits
    str_num = str(num)
    # print(str_num[2])
    num_digits = len(str_num)
    
    # Calculate the sum of each digit raised to the power of num_digits
    # armstrong_sum = sum(int(digit) ** num_digits for digit in str_num)
    armstrong_sum = 0
    
    for digit in str_num:
        # armstrong_sum += int(digit) ** num_digits
        print(f"{digit} The digit type is {type(digit)}")
        armstrong_sum = armstrong_sum + int(digit) ** num_digits
    
    
    
    # Check if the calculated sum is equal to the original number
    return armstrong_sum == num

b = "duytika"
'''
armstrong_sum = 0 + 1 ** 3 + 5 ** 3 + 3 ** 3 =153

digit = 3

num_digits = 3

num = 153


'''
# d | u | y | t | i | k |a
# for character in b:
#     print(f"Location of {character} is at {id(character)}")

str_num = 153


def main():
    # Test the function with some examples
    test_numbers = [153, 370, 371, 9474, 9475, 123]
    for number in test_numbers:
        if isArmstrongNumber(number):
            print(f"{number} is an Armstrong number.")
        else:
            print(f"{number} is not an Armstrong number.")
    print(f"{str_num} is an Armstrong number.")
            
            
            
if __name__ == "__main__":
    main()
  
__doc__
# pi = 3.14159  
# __pi__ = 3.14159
# __author__ = "Your Name"
  
  
  
  
  
  '''
  n=10
  
  n<=1
  
  f(n-1) = 9, 8, 7, 6, 5, 4, 3, 2, 1
  
  f(n-2) = 8, 6, 4, 2, 0
  
  
  '''