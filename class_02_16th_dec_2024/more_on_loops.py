# 1. Prime Factorization with Advanced Tracking
def prime_factorization(n):
    """
    Decompose a number into its prime factors with detailed tracking.
    Returns a dictionary of prime factors and their frequencies.
    """
    factors = {}
    divisor = 2
    
    while divisor * divisor <= n:
        if n % divisor == 0:
            # Count factor frequency
            if divisor not in factors:
                factors[divisor] = 0
            factors[divisor] += 1
            
            # Divide number by the factor
            n //= divisor
        else:
            # Move to next potential divisor
            divisor += 1
    
    # If remaining number is > 1, it's a prime factor itself
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    
    return factors

# 2. Spiral Matrix Generation
def generate_spiral_matrix(n):
    """
    Generate an n x n spiral matrix filled with consecutive numbers.
    """
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Directional vectors for right, down, left, up movement
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    
    x, y = 0, 0  # Starting position
    direction = 0  # Start moving right
    current_num = 1
    
    while current_num <= n * n:
        matrix[y][x] = current_num
        current_num += 1
        
        # Calculate next position
        next_x = x + dx[direction]
        next_y = y + dy[direction]
        
        # Check if next move is valid
        if (0 <= next_x < n and 0 <= next_y < n and 
            matrix[next_y][next_x] == 0):
            x, y = next_x, next_y
        else:
            # Change direction
            direction = (direction + 1) % 4
            x += dx[direction]
            y += dy[direction]
    
    return matrix

# 3. Complex Number Sequence Generator
def generate_complex_sequence(length, start_real, start_imag, rule):
    """
    Generate a complex number sequence based on a custom transformation rule.
    
    Args:
    - length: Number of terms to generate
    - start_real: Initial real part
    - start_imag: Initial imaginary part
    - rule: A function that takes current real and imag parts and returns next values
    
    Returns a list of complex numbers
    """
    sequence = [complex(start_real, start_imag)]
    
    for _ in range(1, length):
        last = sequence[-1]
        next_real, next_imag = rule(last.real, last.imag)
        sequence.append(complex(next_real, next_imag))
    
    return sequence

# 4. Advanced Pattern Matching in Sequence
def find_subsequence_patterns(main_sequence, pattern_length):
    """
    Find all unique subsequences of a given length and their frequencies.
    
    Args:
    - main_sequence: Input sequence to search
    - pattern_length: Length of subsequences to find
    
    Returns a dictionary of subsequences and their frequencies
    """
    pattern_frequencies = {}
    
    for i in range(len(main_sequence) - pattern_length + 1):
        subsequence = tuple(main_sequence[i:i+pattern_length])
        pattern_frequencies[subsequence] = pattern_frequencies.get(subsequence, 0) + 1
    
    return {k: v for k, v in pattern_frequencies.items() if v > 1}

# 5. Dynamic Programming: Longest Increasing Subsequence
def longest_increasing_subsequence(arr):
    """
    Find the longest increasing subsequence using dynamic programming.
    
    Returns:
    - Length of the longest increasing subsequence
    - The actual subsequence
    """
    if not arr:
        return 0, []
    
    # Track length of LIS ending at each index
    lengths = [1] * len(arr)
    # Track previous element index for reconstruction
    prev_indices = [-1] * len(arr)
    
    # Maximum length and its ending index
    max_length = 1
    max_index = 0
    
    # Dynamic programming to find LIS
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[i] > arr[j] and lengths[i] < lengths[j] + 1:
                lengths[i] = lengths[j] + 1
                prev_indices[i] = j
                
                # Update max length tracking
                if lengths[i] > max_length:
                    max_length = lengths[i]
                    max_index = i
    
    # Reconstruct subsequence
    subsequence = []
    while max_index != -1:
        subsequence.insert(0, arr[max_index])
        max_index = prev_indices[max_index]
    
    return max_length, subsequence

# Demonstration of usage
if __name__ == "__main__":
    # 1. Prime Factorization Example
    print("Prime Factorization of 84:", prime_factorization(84))
    
    # 2. Spiral Matrix Example
    print("\nSpiral Matrix (3x3):")
    spiral = generate_spiral_matrix(3)
    for row in spiral:
        print(row)
    
    # 3. Complex Sequence Generator Example
    def complex_rule(real, imag):
        return real * real - imag * imag, 2 * real * imag
    
    complex_seq = generate_complex_sequence(5, 1, 1, complex_rule)
    print("\nComplex Sequence:", complex_seq)
    
    # 4. Pattern Matching Example
    sequence = [1, 2, 3, 1, 2, 3, 4, 1, 2, 3]
    patterns = find_subsequence_patterns(sequence, 3)
    print("\nRepeated Subsequences:", patterns)
    
    # 5. Longest Increasing Subsequence Example
    arr = [10, 22, 9, 33, 21, 50, 41, 60, 80]
    lis_length, lis_subsequence = longest_increasing_subsequence(arr)
    print("\nLongest Increasing Subsequence:")
    print("Length:", lis_length)
    print("Subsequence:", lis_subsequence)