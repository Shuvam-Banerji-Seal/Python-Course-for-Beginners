import random
import math
import matplotlib.pyplot as plt

class my_class:
    def __init__(self, value):
        self.value = value

    def compute_square_root(self):
        return math.sqrt(self.value)

    def compute_power(self, exponent):
        return math.pow(self.value, exponent)

    def compute_logarithm(self, base):
        return math.log(self.value, base)
    
    def compute_factorial(self):
        return math.factorial(self.value)
    
    def compute_sine(self):
        return math.sin(self.value)

    def sample_random_functions(self):
        # Generate a random float between 0.0 and 1.0
        random_float = random.random()
        print(f"Random float between 0.0 and 1.0: {random_float}")

        # Generate a random integer between 1 and 10 (inclusive)
        random_int = random.randint(1, 10)
        print(f"Random integer between 1 and 10: {random_int}")

        # Choose a random element from a list
        sample_list = ['apple', 'banana', 'cherry', 'date']
        random_choice = random.choice(sample_list)
        print(f"Random choice from list: {random_choice}")

        # Shuffle a list in place
        random.shuffle(sample_list)
        print(f"Shuffled list: {sample_list}")

        # Generate a random sample of 2 elements from the list
        random_sample = random.sample(sample_list, 2)
        print(f"Random sample of 2 elements: {random_sample}")

        # Plotting random values
        random_values = [random.random() for _ in range(10)]
        plt.plot(random_values, marker='o')
        plt.title("Random Values")
        plt.xlabel("Index")
        plt.ylabel("Random Value")
        plt.show()


if __name__ == "__main__":
    obj = my_class(16)
    print(f"Square root of {obj.value}: {obj.compute_square_root()}")
    print(f"{obj.value} raised to the power of 3: {obj.compute_power(3)}")
    print(f"Logarithm of {obj.value} with base 2: {obj.compute_logarithm(2)}")
    print(f"Factorial of {obj.value}: {obj.compute_factorial()}")
    print(f"Sine of {obj.value}: {obj.compute_sine()}")

    print("\nSampling random functions:")
    obj.sample_random_functions()



