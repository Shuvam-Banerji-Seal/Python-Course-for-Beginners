def sieve_of_eratosthenes_detailed(n):
    """
    Detailed implementation of Sieve of Eratosthenes with step-by-step explanation
    
    Args:
        n (int): Upper limit for finding prime numbers
    
    Returns:
        list: List of prime numbers up to n
    """
    # Step 1: Create a boolean array to track prime numbers
    # Initially, assume all numbers are prime
    is_prime = [True] * (n + 1)
    
    # Step 2: Mark 0 and 1 as not prime
    is_prime[0] = False
    is_prime[1] = False
    
    # Step 3: Apply the Sieve algorithm
    # Only need to check up to square root of n
    for current_number in range(2, int(n**0.5) + 1):
        # If current number is marked prime
        if is_prime[current_number]:
            # Mark all multiples of this number as not prime
            # Start from current_number * current_number 
            # (smaller multiples would have been marked earlier)
            for multiple in range(current_number * current_number, n + 1, current_number):
                is_prime[multiple] = False
    
    # Step 4: Collect and return prime numbers
    primes = [num for num in range(2, n + 1) if is_prime[num]]
    return primes

def visualize_sieve_process(n):
    """
    Visualize the Sieve of Eratosthenes process
    
    Args:
        n (int): Upper limit for finding prime numbers
    """
    # Create a boolean array to track prime numbers
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    print(f"Finding primes up to {n}:\n")
    
    # Detailed step-by-step visualization
    for current_number in range(2, int(n**0.5) + 1):
        if is_prime[current_number]:
            print(f"\nProcessing number {current_number}:")
            print(f"  - {current_number} is prime")
            print(f"  - Marking multiples of {current_number}:")
            
            # Mark multiples
            for multiple in range(current_number * current_number, n + 1, current_number):
                if is_prime[multiple]:
                    print(f"    * Marking {multiple} as not prime")
                is_prime[multiple] = False
    
    # Collect and print prime numbers
    primes = [num for num in range(2, n + 1) if is_prime[num]]
    print("\nFinal Prime Numbers:")
    print(primes)

def explain_sieve_algorithm():
    """
    Comprehensive explanation of the Sieve of Eratosthenes algorithm
    """
    print("Sieve of Eratosthenes: Prime Number Generation Algorithm\n")
    
    print("Algorithm Stages:")
    print("1. Initialization")
    print("   - Create a boolean array of size n+1")
    print("   - Initially mark all numbers as potentially prime")
    print("   - Explicitly mark 0 and 1 as not prime\n")
    
    print("2. Sieving Process")
    print("   - Iterate through numbers from 2 to sqrt(n)")
    print("   - If a number is prime:")
    print("     a. Keep it as prime")
    print("     b. Mark all its multiples as not prime")
    print("     c. Start marking from number * number")
    print("     d. Increment by the number itself\n")
    
    print("3. Prime Collection")
    print("   - Collect all numbers still marked as prime")
    print("   - These are the prime numbers up to n\n")
    
    print("Time Complexity: O(n log log n)")
    print("Space Complexity: O(n)")

# Demonstration and Explanation
def main():
    print("Sieve of Eratosthenes Demonstration\n")
    
    # Find primes up to 30
    n = 30
    
    print("Visualization of Sieve Process:")
    visualize_sieve_process(n)
    
    print("\n\nDetailed Algorithm Explanation:")
    explain_sieve_algorithm()

# Run the main demonstration
if __name__ == "__main__":
    main()