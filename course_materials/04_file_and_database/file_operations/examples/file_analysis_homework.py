#!/usr/bin/env python3
"""
File Analysis Homework Solutions
Based on the homework assignments from the original course.

This module provides functions to analyze various aspects of text files:
- Count words, lines, characters
- Count sentences, vowels, consonants
- Count uppercase letters, digits, spaces, tabs, newlines
- Count punctuation marks
"""

import string
import re
from pathlib import Path

def count_words(filepath):
    """Count the number of words in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split by whitespace and filter out empty strings
            words = [word for word in content.split() if word.strip()]
            return len(words)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_lines(filepath):
    """Count the number of lines in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_characters(filepath, include_whitespace=True):
    """Count the number of characters in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            if include_whitespace:
                return len(content)
            else:
                # Count only non-whitespace characters
                return len([char for char in content if not char.isspace()])
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_sentences(filepath):
    """Count the number of sentences in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            # Use regex to find sentence endings
            sentences = re.findall(r'[.!?]+', content)
            return len(sentences)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_vowels(filepath):
    """Count the number of vowels in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            vowels = 'aeiou'
            count = sum(1 for char in content if char in vowels)
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_consonants(filepath):
    """Count the number of consonants in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().lower()
            vowels = 'aeiou'
            count = sum(1 for char in content if char.isalpha() and char not in vowels)
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_uppercase_letters(filepath):
    """Count the number of uppercase letters in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            count = sum(1 for char in content if char.isupper())
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_digits(filepath):
    """Count the number of digits in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            count = sum(1 for char in content if char.isdigit())
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_spaces(filepath):
    """Count the number of spaces in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            count = content.count(' ')
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_tabs(filepath):
    """Count the number of tabs in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            count = content.count('\t')
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_newlines(filepath):
    """Count the number of newline characters in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            count = content.count('\n')
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def count_punctuation(filepath):
    """Count the number of punctuation marks in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            count = sum(1 for char in content if char in string.punctuation)
            return count
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

def analyze_file_comprehensive(filepath):
    """Perform comprehensive analysis of a file"""
    print(f"📊 Comprehensive Analysis of: {filepath}")
    print("=" * 60)
    
    if not Path(filepath).exists():
        print(f"❌ File does not exist: {filepath}")
        return
    
    # Collect all statistics
    stats = {
        'Words': count_words(filepath),
        'Lines': count_lines(filepath),
        'Characters (total)': count_characters(filepath, True),
        'Characters (no whitespace)': count_characters(filepath, False),
        'Sentences': count_sentences(filepath),
        'Vowels': count_vowels(filepath),
        'Consonants': count_consonants(filepath),
        'Uppercase letters': count_uppercase_letters(filepath),
        'Digits': count_digits(filepath),
        'Spaces': count_spaces(filepath),
        'Tabs': count_tabs(filepath),
        'Newlines': count_newlines(filepath),
        'Punctuation marks': count_punctuation(filepath)
    }
    
    # Display results
    for category, count in stats.items():
        print(f"{category:25}: {count:6,}")
    
    # Additional insights
    print("\n📈 Additional Insights:")
    if stats['Words'] > 0:
        avg_word_length = stats['Characters (no whitespace)'] / stats['Words']
        print(f"Average word length      : {avg_word_length:.2f} characters")
    
    if stats['Lines'] > 0:
        avg_words_per_line = stats['Words'] / stats['Lines']
        print(f"Average words per line   : {avg_words_per_line:.2f}")
    
    if stats['Sentences'] > 0:
        avg_words_per_sentence = stats['Words'] / stats['Sentences']
        print(f"Average words per sentence: {avg_words_per_sentence:.2f}")
    
    # Character composition
    total_letters = stats['Vowels'] + stats['Consonants']
    if total_letters > 0:
        vowel_percentage = (stats['Vowels'] / total_letters) * 100
        print(f"Vowel percentage         : {vowel_percentage:.1f}%")

def create_sample_file():
    """Create a sample file for testing"""
    sample_content = """Hello World! This is a sample text file.
It contains multiple lines, sentences, and various characters.
We have UPPERCASE letters, lowercase letters, numbers like 123 and 456.
There are punctuation marks: periods, commas, exclamation points!
Some lines have	tabs	and   multiple   spaces.

This file is perfect for testing our file analysis functions.
Let's see how many words, characters, and other elements it contains?
The analysis should provide comprehensive statistics about this text."""
    
    filepath = 'sample_files/analysis_sample.txt'
    Path('sample_files').mkdir(exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    
    print(f"✅ Created sample file: {filepath}")
    return filepath

def demonstrate_all_functions():
    """Demonstrate all analysis functions"""
    print("🔍 File Analysis Homework Solutions")
    print("=" * 50)
    
    # Create a sample file
    sample_file = create_sample_file()
    
    # Test each function individually
    print(f"\n📋 Individual Function Tests:")
    print(f"Words: {count_words(sample_file)}")
    print(f"Lines: {count_lines(sample_file)}")
    print(f"Characters: {count_characters(sample_file)}")
    print(f"Sentences: {count_sentences(sample_file)}")
    print(f"Vowels: {count_vowels(sample_file)}")
    print(f"Consonants: {count_consonants(sample_file)}")
    print(f"Uppercase letters: {count_uppercase_letters(sample_file)}")
    print(f"Digits: {count_digits(sample_file)}")
    print(f"Spaces: {count_spaces(sample_file)}")
    print(f"Tabs: {count_tabs(sample_file)}")
    print(f"Newlines: {count_newlines(sample_file)}")
    print(f"Punctuation: {count_punctuation(sample_file)}")
    
    # Comprehensive analysis
    print(f"\n")
    analyze_file_comprehensive(sample_file)

def main():
    """Main function to run the demonstrations"""
    demonstrate_all_functions()
    
    print(f"\n💡 Usage Examples:")
    print(f"   from file_analysis_homework import count_words")
    print(f"   word_count = count_words('my_file.txt')")
    print(f"   analyze_file_comprehensive('my_file.txt')")

if __name__ == "__main__":
    main()