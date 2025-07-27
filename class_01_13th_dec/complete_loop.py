# Range-based for loop
def basic_range_loop():
    for i in range(5):
        print(i)

# List iteration
def list_iteration():
    fruits = ['apple', 'banana', 'cherry']
    for fruit in fruits:
        print(fruit)
        
        
def while_loop_example():
    count = 0
    while count < 5:
        print(count)
        count += 1
        
def enumerate_loop():
    languages = ['Python', 'Java', 'C++']
    for index, language in enumerate(languages):
        print(f"Index {index}: {language}")
        
        
def nested_loops():
    for i in range(3):
        for j in range(3):
            print(f"({i}, {j})", end=" ")
        print()
        
def list_comprehension_examples():
    # Basic comprehension
    squares = [x**2 for x in range(5)]
    print("Squares:", squares)
    
    # Comprehension with condition
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print("Even Squares:", even_squares)

def generator_expressions():
    # Memory efficient generation of values
    gen = (x**2 for x in range(5))
    print("Generator:", list(gen))
    
    
def main():
    basic_range_loop()
    list_iteration()
    while_loop_example()
    enumerate_loop()
    nested_loops()
    list_comprehension_examples()
    generator_expressions()
    

if __name__ == "__main__":
    main()