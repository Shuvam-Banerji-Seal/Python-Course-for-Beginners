# File Programming Homework Solutions

This document provides solutions to the homework problems from the original course, with enhanced explanations and additional challenges.

## 📝 Original Homework Problems

The original homework asked students to create functions to find:

1. ✅ Number of words in a file
2. ✅ Number of lines in a file  
3. ✅ Number of characters in a file
4. ✅ Number of sentences in a file
5. ✅ Number of vowels in a file
6. ✅ Number of uppercase letters in a file
7. ✅ Number of consonants in a file
8. ✅ Number of digits in a file
9. ✅ Number of spaces in a file
10. ✅ Number of tabs in a file
11. ✅ Number of new lines in a file
12. ✅ Number of punctuation marks in a file

## 🚀 Enhanced Solutions

All solutions are implemented in `../examples/file_analysis_homework.py` with the following improvements:

### 1. Proper Error Handling
```python
def count_words(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            words = [word for word in content.split() if word.strip()]
            return len(words)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return 0
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0
```

### 2. Unicode Support
All functions properly handle international characters using UTF-8 encoding.

### 3. Comprehensive Analysis
The `analyze_file_comprehensive()` function provides:
- All basic counts
- Additional insights (averages, percentages)
- Performance metrics
- Error handling

## 🧪 Testing Your Solutions

### Create Test Files
```python
# Create a test file
test_content = """Hello World! This is a test.
It has UPPERCASE and lowercase letters.
Numbers: 123, 456, 789.
Punctuation: !@#$%^&*()
Tabs:	here	and	here
Multiple   spaces   here.

Empty line above and special chars: café, naïve."""

with open('test_file.txt', 'w', encoding='utf-8') as f:
    f.write(test_content)
```

### Run Analysis
```python
from file_analysis_homework import analyze_file_comprehensive
analyze_file_comprehensive('test_file.txt')
```

## 📊 Expected Results for Test File

For the test content above, you should get approximately:
- **Words**: 25-30 (depending on how you count)
- **Lines**: 8
- **Characters**: ~200 (including whitespace)
- **Sentences**: 4 (based on periods, exclamation marks)
- **Vowels**: ~60-70
- **Consonants**: ~80-90
- **Uppercase**: ~10-15
- **Digits**: 9 (1,2,3,4,5,6,7,8,9)
- **Spaces**: ~25-30
- **Tabs**: 3
- **Newlines**: 7
- **Punctuation**: ~15-20

## 🎯 Additional Challenges

### Challenge 1: Advanced Word Counting
Modify the word counting function to:
- Ignore punctuation when counting words
- Handle contractions properly (don't → don't counts as 1 word)
- Count hyphenated words correctly

### Challenge 2: Language Detection
Create a function that analyzes character frequency to guess the language:
```python
def guess_language(filepath):
    # Analyze character frequency patterns
    # Return likely language based on common letter patterns
    pass
```

### Challenge 3: File Comparison
Create a function that compares two files and reports:
- Which file has more words/characters
- Common words between files
- Unique words in each file

### Challenge 4: Performance Optimization
Optimize the analysis functions for very large files:
- Process files line by line instead of loading entirely
- Use generators for memory efficiency
- Add progress reporting for long operations

## 🔧 Usage Examples

### Basic Usage
```python
from file_analysis_homework import count_words, count_lines

word_count = count_words('my_file.txt')
line_count = count_lines('my_file.txt')
print(f"File has {word_count} words and {line_count} lines")
```

### Comprehensive Analysis
```python
from file_analysis_homework import analyze_file_comprehensive

# Analyze any text file
analyze_file_comprehensive('README.md')
analyze_file_comprehensive('my_essay.txt')
analyze_file_comprehensive('code_file.py')
```

### Batch Analysis
```python
import os
from file_analysis_homework import analyze_file_comprehensive

# Analyze all .txt files in a directory
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        print(f"\n{'='*50}")
        print(f"Analyzing: {filename}")
        print('='*50)
        analyze_file_comprehensive(filename)
```

## 💡 Learning Objectives Achieved

By completing these homework problems, students learn:

1. **File I/O fundamentals** - Opening, reading, and closing files properly
2. **String processing** - Analyzing text content programmatically  
3. **Error handling** - Dealing with missing files and encoding issues
4. **Unicode awareness** - Handling international characters correctly
5. **Performance considerations** - Processing large files efficiently
6. **Code organization** - Writing reusable, well-documented functions
7. **Testing and validation** - Verifying results with known test cases

## 🚀 Next Steps

After mastering these basic file analysis tasks, students can explore:
- **Regular expressions** for more sophisticated text pattern matching
- **Natural language processing** libraries like NLTK or spaCy
- **Data visualization** of text analysis results
- **Web scraping** and analyzing online text content
- **Machine learning** applications for text classification

The homework solutions provide a solid foundation for more advanced text processing and file manipulation tasks!