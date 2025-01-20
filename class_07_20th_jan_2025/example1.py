def sort_by_vowel_count(sentence):

    # Define vowels as a list
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    
    # Function to count vowels in a word
    def count_vowels(word):
        return sum(1 for char in word if char in vowels)
    
    # Split sentence into words
    words = sentence.split()
    
    # Sort words based on vowel count
    sorted_words = sorted(words, key=count_vowels)
    
    # Join words back into sentence
    return ' '.join(sorted_words)

# Example usage
if __name__ == "__main__":
    test_sentence = "Rajiv has cracked a dictionary"
    result = sort_by_vowel_count(test_sentence)
    print(f"Original: {test_sentence}")
    print(f"Sorted: {result}")