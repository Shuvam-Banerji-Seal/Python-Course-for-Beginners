# Python script demonstrating various print() methods, string comprehension, 
# different operators, arguments, and vulnerabilities of print()

def print_basics():
    print("\n=== Basic Print Statements ===")
    print("Hello, World!")  # Simple string print
    print(100)  # Printing an integer
    print(3.14)  # Printing a float
    print(True)  # Printing a boolean
    print("Hello", "World", 123, sep=" - ")  # Multiple arguments with separator

def print_with_formatting():
    print("\n=== Print with Formatting ===")
    name, age = "Alice", 25
    print("Name: {}, Age: {}".format(name, age))  # Using format()
    print(f"Name: {name}, Age: {age}")  # Using f-string
    print("Name: %s, Age: %d" % (name, age))  # Using old-style formatting

def print_string_comprehensions():
    print("\n=== String Comprehensions ===")
    words = ["apple", "banana", "cherry"]
    print(" ".join(words))  # Joining list elements into a string
    print("-".join([word.upper() for word in words]))  # Upper case join

def print_special_characters():
    print("\n=== Special Characters in Print ===")
    print("Hello\nWorld")  # Newline
    print("Hello\tWorld")  # Tab space
    print("C:\\Users\\Alice")  # Escape backslashes

def print_with_end():
    print("\n=== Print with End Parameter ===")
    print("Start", end=" - ")
    print("Middle", end="... ")
    print("End")  # Prints in a single line with specified end

def print_to_file():
    print("\n=== Print to File ===")
    with open("output.txt", "w") as file:
        print("Writing to a file", file=file)
    print("Check 'output.txt' for output.")

def print_vulnerabilities():
    print("\n=== Print Vulnerabilities ===")
    # Example of accidental information leak
    sensitive_data = {"username": "admin", "password": "secret123"}
    print("Logging info:", sensitive_data)  # Can expose sensitive data if misused
    
    # Example of code execution via eval
    user_input = "__import__('os').system('ls')"  # Malicious input
    try:
        print("Evaluating user input (unsafe):", eval(user_input))
    except Exception as e:
        print("Blocked potential vulnerability:", e)
    
    # Prevent this by sanitizing input or avoiding eval() entirely

def main():
    print_basics()
    print_with_formatting()
    print_string_comprehensions()
    print_special_characters()
    print_with_end()
    print_to_file()
    print_vulnerabilities()

if __name__ == "__main__":
    main()
  
