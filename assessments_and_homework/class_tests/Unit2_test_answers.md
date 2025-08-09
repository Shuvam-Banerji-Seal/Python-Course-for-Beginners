# Answer Sheet for Unit 2 Test

This document provides the answers to the "Computational Thinking and Programming - I" mock test.

---

## Questions & Answers

### Introduction to Problem-solving

1.  **C) Diamond (Decision):** The diamond shape is used in flowcharts to represent a decision point.
2.  **A) A=10, B=20, C=30:** The pseudocode fails when C is the largest number. The logic doesn't handle the case where `B > C` is false within the `ELSE` block, so nothing is printed.
3.  **A) Decomposition:** This is the process of breaking down a complex problem into smaller, more manageable parts.

### Familiarization with the basics of Python programming

4.  **C) After the British comedy troupe "Monty Python's Flying Circus":** Guido van Rossum was a fan of the show.
5.  **C) 2nd_variable:** Variable names in Python cannot begin with a number.
6.  **B) Interactive mode executes commands immediately, while script mode saves commands in a file for later execution.**
7.  **B) An r-value:** The right-hand side of an assignment is an r-value, representing the value to be assigned.

### Knowledge of data types

8.  **D) Tuple:** Tuples are immutable, meaning their contents cannot be changed after creation.
9.  **B) [1, 2, [5, 4]]:** `y = x.copy()` creates a shallow copy. The nested list `[3, 4]` is a reference. Modifying it in `y` also changes it in `x`.
10. **D) boolean:** The boolean data type stores `True` or `False`.
11. **B) True, False:** `a == b` is `True` because the values are equal. `a is b` is `False` because they are different objects in memory (an `int` and a `float`).

### Operators

12. **A) 2:** Due to operator precedence, `3 ** 2` is 9. Then `10 // 9` is 1. Finally, `1 * 2` is 2.
13. **B) 11:** `3 * 2` is 6. The expression becomes `x = 5 + 6`, which is 11.
14. **A) not (5 > 3 and 2 > 3) and (2 < 3 or 2 > 1):** This evaluates to `not (True and False) and (True or True)`, which is `True and True`, resulting in `True`.
15. **B) True, False:** The `in` operator is case-sensitive. 'p' is in 'python', but 'P' is not.

### Expressions, statement, type conversion, and input/output

16. **B) int('10'):** This is an explicit conversion from a string to an integer.
17. **B) 20.0:** `int(10.7)` is `10`. `float(10)` is `10.0`. The sum is `20.0`.
18. **B) 4242:** The `input()` function returns a string. Multiplying the string '42' by 2 results in string concatenation: '4242'.

### Errors

19. **C) Logical Error:** A logical error occurs when the code runs but does not produce the intended result.
20. **B) ZeroDivisionError:** Division by zero is not allowed and raises this specific runtime error.

### Flow of Control - Conditional statements

21. **B) Zero:** The condition `x == 0` is true, so "Zero" is printed.
22. **D) A nested if-elif-else structure:** This is the most appropriate and clear way to handle multiple distinct cases for sorting three numbers.

### Flow of Control - Iterative Statement

23. **B) 1 3 5:** `range(1, 6, 2)` starts at 1, goes up to (but not including) 6, with a step of 2.
24. **B) 6:** The outer loop runs 3 times, and the inner loop runs 2 times for each outer iteration (3 * 2 = 6).
25. **A) 4 3 1 0:** The loop prints `i` after decrementing. When `i` becomes 2, `continue` skips the `print` statement for that iteration.
26. **B) while True:** This is the standard idiom for creating an infinite loop in Python.

### Modules (`math`, `random`, `statistics`)

27. **B) sqrt(16):** When a function is imported directly using `from math import sqrt`, it can be called without the module prefix.
28. **C) It provides a shorter alias, which is useful for long module names.**
29. **B) It can lead to name clashes if functions from the module have the same name as variables in your code.**
30. **B) Radians:** Trigonometric functions in the `math` module use radians for their calculations.
31. **B) 6 5:** `math.ceil(5.2)` rounds up to 6. `math.floor(5.8)` rounds down to 5.
32. **D) int, float:** The `**` operator returns an `int` if both operands are integers. `math.pow()` always returns a `float`.
33. **C) A ValueError:** The square root of a negative number is not defined for real numbers, so `math.sqrt` raises a `ValueError`.
34. **C) math.fabs(-20):** `math.fabs()` returns the absolute value as a float (`20.0`). `abs(-20)` would return an integer (`20`).
35. **D) A terrible idea that almost never works:** This is a humorous question about bad debugging practices.
36. **C) random.randint(1, 10):** `randint(a, b)` returns a random integer N such that a <= N <= b.
37. **D) random.randint(5, 10):** This is the only option that includes 5 in its possible range.
38. **B) randint includes b in the range, while randrange does not.** `randrange(a, b)` is exclusive of `b`.
39. **B) random.choice(["Heads", "Tails"]):** This is the most direct and readable way to choose between two string options.
40. **B) A random floating point number in the range [0.0, 1.0).**
41. **A) 25.0:** The mean is the sum (100) divided by the count (4). The `statistics.mean` function returns a float.
42. **B) 5:** First, sort the list: `[1, 2, 5, 8, 9]`. The median is the middle element.
43. **D) A StatisticsError:** The `statistics.mode` function raises an error if the data has more than one mode (both 2 and 3 appear twice).
44. **A) mean > median > mode:** The mean is (1+1+2+5+6)/5 = 3. The median is 2. The mode is 1. So, 3 > 2 > 1.
45. **A) 7:** The list comprehension filters for numbers greater than 5 (`[9, 16]`), calculates their square roots (`[3.0, 4.0]`), converts them to integers (`[3, 4]`), and `sum()` adds them to get 7.
46. **B) z1:** `random.choice(chars)` will be 'x', 'y', or 'z'. `random.randint(1,1)` will always be 1. So 'z1' is a possible output.
47. **A) 5:** `math.log10(100)` is 2.0, `int(2.0)` is 2. `math.floor(3.14)` is 3. `2 + 3 = 5`.
48. **D) statistics.mean(L):** `sum([])` is 0, `len([])` is 0, and `sorted([])` is `[]`. But finding the mean of an empty list is a mathematical error.
49. **D) random.choice([2, 4, 6, 8, 10]):** This is the most direct way. `random.randrange(2, 11, 2)` also works correctly.
50. **B) 3.0:** `math.factorial(4)` is 24. `math.pow(2, 3)` is 8.0. `24 / 8.0` is `3.0`.

### Mixed/Tricky Questions

51. **B) 55:** The loop runs from `i = 0` to `i = 49`. `x` is not decremented when `i` is a multiple of 10 (0, 10, 20, 30, 40). So, `x` is decremented `50 - 5 = 45` times. `100 - 45 = 55`.
52. **B) Rubber Duck Debugging:** This is a real and effective method for debugging code.
53. **B) c 3:** The dictionary value for the key `(1, 2)` is updated to 'c'. The value for 'key' is updated to the tuple `(3, 4)`. The output is the new value 'c' and the first element of the new tuple, 3.
54. **A) Python is fun:** `.strip()` removes whitespace. `.capitalize()` makes the first character uppercase and the rest lowercase. `.replace()` substitutes the underscore.
55. **D) a is b:** Python caches small integers (-5 to 256). `x` and `y` (5) point to the same object. `a` and `b` (257) are outside this range and are created as separate objects. Thus `a is b` is `False`.
56. **A) [1, 3, 5]:** **This is a classic tricky question.** Modifying a list while iterating over it causes the iterator to skip elements. When 2 is removed, the list becomes `[1, 3, 4, 5]`, and the next item processed is 4 (it skips 3). When 4 is removed, the list is `[1, 3, 5]` and the loop ends.
57. **B) b:** `d.items()` is sorted by key, resulting in `[('a', 2), ('b', 1), ('c', 0)]`. The item at index 1 is `('b', 1)`, and its first element is `'b'`.
58. **D) Raise a ValueError:** Factorial is not defined for negative numbers.
59. **C) 25:** The loop adds `i` to `result` for `i` = 1, 3, 5, 7, 9. The sum is `1 + 3 + 5 + 7 + 9 = 25`.
60. **D) An assignment statement like x = y + 1:** A rectangle in a flowchart represents a process or an action, such as a calculation and assignment.
61. **A) (10, 20, [35, 40]):** A tuple is immutable, but the list object inside it is mutable. You can change the contents of the list.
62. **A) The l-value must be a memory location, while the r-value must be a value.**
63. **C) False False True:** `None` and empty containers (`[]`) are falsy. A non-empty string, even 'False', is truthy.
64. **B) int, 1000000:** Underscores in numeric literals are for readability and are ignored by the interpreter.
65. **B) 0 1 Loop finished!:** The `else` block of a `for` loop executes when the loop completes normally (without a `break`).
66. **C) 0 1 2:** The `break` statement terminates the loop, so the `else` block is not executed.
67. **C) tuple:** The `partition` method returns a tuple of three strings.
68. **D) s.split():** The `split` method always returns a list of strings.
69. **B) [[5, 2], [3, 4]]:** `z` contains a reference to the list `x`. When `x[0]` is changed, that change is reflected in `z`.
70. **A) employees.insert(2, 'David'):** This inserts 'David' at index 2, shifting the subsequent elements.
71. **B) 2 3:** In Python dictionaries, the integer key `1` and the float key `1.0` are treated as equal. The assignment `d[1.0] = 3` overwrites the value for the key `1`. The string `'1'` is a distinct key.
72. **C) pop():** `d.pop(key)` removes the key and returns its value, raising a `KeyError` if the key is not found.
73. **D) A StatisticsError is raised:** The data is multimodal ('cat' and 'dog' appear twice), which causes `statistics.mode` to raise an error.
74. **B) 40:** Slicing `L[1:4]` gives `[20, 30, 40]`. With `random.seed(42)`, `random.choice` on this list will always pick `40`.
75. **A) True:** Operator precedence is `not`, then `and`, then `or`. The expression becomes `True or (False and False)`, which is `True or False`, resulting in `True`.
76. **C) As a placeholder for code they intend to write later, to avoid syntax errors.**
77. **C) hello world:** String methods like `upper()` return a *new* string and do not modify the original. The original `msg` ("hello") is used in the concatenation.
78. **C) "Error":** `statistics.mean` cannot handle a string ('5') in the data, so it raises a `TypeError`, which is caught by the `except` block.
79. **A) True:** `t` becomes `(1, 2, 3, 1, 2, 3)` and `L` becomes `[1, 2, 3, 1, 2, 3]`. `t[3]` is `1` and `L[3]` is `1`. `1 == 1` is `True`.
80. **D) A list:** Dictionary keys must be of an immutable type. Lists are mutable.

### Final Set - More Tricky/Comprehensive Questions

81. **B) 6:** Precedence: `1**2` is 1. Then `5*1` is 5. Then `3//2` is 1. Finally `5 + 1` is 6.
82. **A) 'fd':** Slicing `s[5:1:-2]` starts at index 5 ('f'), goes towards index 1 (exclusive), with a step of -2. It gets the character at index 5 ('f') and index 3 ('d').
83. **C) 10 15:** `x, y = y, x` swaps them, so `x` becomes 20 and `y` becomes 10. Then `x = x - 10` makes `x` 10. Then `y = y + 5` makes `y` 15.
84. **C) Line 3:** `my_list` has indices 0, 1, and 2. Accessing `my_list[3]` will cause an `IndexError`.
85. **C) "Oh, that's why my fan is so loud.":** A humorous take on a common symptom of an infinite loop consuming CPU resources.
86. **C) {'a': 1, 'b': 2, 'c': 3}:** `zip` creates pairs for the shorter iterable, so `dict` creates `{'a': 1, 'b': 2}`. Then the key 'c' is added with the value 3.
87. **C) 0 1 2:** The loop prints 0, 1, 2. When `i` becomes 3, the `break` statement is executed, terminating the loop. The `else` block is skipped.
88. **B) (False, True, True):** `None == 0` is `False`. `None is None` is always `True`. `None == None` is also `True`.
89. **B) ([1, 3], [2]):** `t` is a tuple containing two lists. `L` is a reference to the first list. Appending to `L` modifies that list in place. Since the tuple `t` holds a reference to this modified list, its "content" appears to change.
90. **A) 0:** `"".join([])` creates an empty string `""`. The length of an empty string is 0.
91. **A) False True True:** `mystery("Hello World")` is `False` (contains space but isn't only space). `mystery("HelloWorld1")` is `True` (`isalnum`). `mystery("   ")` is `True` (`isspace`).
92. **A) 11:** `math.pow(2, 3.5)` is approximately 11.3137. `int()` truncates the decimal part, resulting in 11.
93. **B) s.startswith(('http', 'https')):** The `startswith` method can accept a tuple of prefixes, which is the most efficient and Pythonic way.
94. **D) 10:** The inner loop runs `0 + 1 + 2 + 3 + 4 = 10` times in total.
95. **C) x, y = 1, 2, 3:** This will raise a `ValueError` because the number of variables to unpack (2) does not match the number of values (3).
96. **C) 30:** For an even-sized dataset, the median is the average of the two middle numbers. Sorted: `[10, 20, 40, 50]`. Median = `(20 + 40) / 2 = 30`.
97. **C) False True True:** `a` and `b` are two separate list objects, so `a is b` is `False`. They contain the same elements, so `a == b` is `True`. `c` is assigned to `a`, so they are the same object, `a is c` is `True`.
98. **C) It solves a complex problem in a simple, clear, and efficient way.**
99. **B) 4:** `L2` is a shallow copy of `L1`. `L` contains references to both lists. `L1[1] = 4` modifies `L1` only. `L[0]` is `L1`, so `L[0][1]` is 4.
100. **A) An even number from 2 to 10 inclusive:** `randrange(start, stop, step)` generates numbers from `start` down by `step` until it's less than `stop`. It will generate 10, 8, 6, 4, 2.
101. **A) 1:** `s.find('y', 1, 2)` searches for 'y' within the slice `s[1:2]`, which is 'y'. It is found, and `find` returns the index within the original string, which is 1.
102. **D) All of the above are valid and reasonably Pythonic.** All three methods achieve the same result effectively.
103. **C) It is a statement that can remove items from a list/dictionary or unbind a variable.**
104. **B) 'banana':** The `key=len` argument tells `max` to compare the items based on their length. 'banana' (length 6) is longer than 'apple' (length 5).
105. **B) {'a': 1, 'b': 3, 'c': 4}:** `update` modifies the dictionary in place. It updates the value for key 'b' and adds the new key-value pair 'c': 4.
106. **B) Pseudocode is textual, while a flowchart is a graphical representation of logic.**
107. **B) False:** This is an example of operator chaining. It is evaluated as `(1 > 2) and (2 == False)`. Since `1 > 2` is `False`, the entire expression is `False`.
108. **C) Choosing a cloud provider:** This is related to infrastructure and deployment, not the fundamentals of problem-solving logic.
109. **B) 1:** `random.random()` returns a float in the range `[0.0, 1.0)`. `math.ceil(x)` for any `x` in `(0.0, 1.0)` is `1`. While `math.ceil(0.0)` is `0`, the probability of `random.random()` returning exactly `0.0` is negligible. Therefore, the overwhelmingly likely result is 1.
110. **D) Coffee. (And sometimes pizza):** A classic programmer joke.

---
### Extra Questions

1.  **B) False:** Due to floating-point precision limitations, `0.1 + 0.2` is not exactly `0.3`.
2.  **B) [1, 3, 2]:** `x.pop(1)` removes `2` and returns it. The list becomes `[1, 3]`. Then `append(2)` adds it to the end.
3.  **B) 3:** The first `'l'` is at index 2. The search for the next one starts at index 3 and finds it at index 3.
4.  **A) True:** Any non-empty string evaluates to `True` in a boolean context.
5.  **A) {'a': 1, 'b': 2, 'c': 3}:** `setdefault` only sets the value if the key is not already present. It adds `'c'` but does not change the existing `'a'`.
6.  **A) 18:** Operator precedence dictates that `3 ** 2` (9) is calculated before `2 * 9` (18).
7.  **C) Error:** Tuples are immutable and do not support item assignment, which will raise a `TypeError`.
8.  **B) heLlo:** The count argument `1` limits the replacement to only the first occurrence of `"l"`.
9.  **B) [1, 2, 3, 4]:** `b = a` creates a reference, not a copy. Modifying `b` also modifies `a`.
10. **B) False:** `1` is an `int`, not an instance of the `float` class.
11. **A) ['a', 'b,c']:** The `maxsplit=1` argument tells `split` to only split the string once.
12. **A) True:** In comparisons, `True` is treated as `1` and `False` is treated as `0`.
13. **B) 0:** The `get` method returns the default value (the second argument, `0`) if the key is not found.
14. **A) abcabcabcxyz:** The `*` operator repeats the string, and `+` concatenates it with the other string.
15. **A) {1, 2, 3, 4, 5}:** `union` combines the sets, automatically handling duplicate elements.
16. **B) 2:** `int(string, base)` converts the string from the given base. "10" in base 2 is 2.
17. **B) False:** `a[:]` creates a shallow copy of the list. `a` and `b` are different objects in memory.
18. **A) ('Hello', ',', ' World!'):** `partition` splits the string at the first occurrence of the separator and returns a 3-tuple.
19. **B) 2 1:** The function prints its local variable `a` (2). The `print` statement outside the function prints the global variable `a` (1).
20. **A) True:** `float('inf')` represents infinity, which is greater than any finite number, including the largest representable standard float.
21. **A) [1]:** `del a[1:]` deletes all elements from index 1 to the end of the list.
22. **A) **abc:** `rjust` right-justifies the string within a field of the given width, padding with the specified character.
23. **A) True:** All elements of set `a` are present in set `b`.
24. **C) (0+13j):** `(2+3j) * (3+2j) = 6 + 4j + 9j + 6j² = 6 + 13j - 6 = 13j`.
25. **A) [1, 2, 3, 4, 5, 6]:** The `+` operator concatenates two lists.
26. **A) 2:** In Python 3, `round()` with a `.5` value rounds to the nearest even integer.
27. **A) 000hello:** `zfill` pads the string on the left with zeros to reach the desired width.
28. **B) False:** `1 == True` evaluates to `True`, so `1 != True` is `False`.
29. **A) []:** `clear()` removes all elements from the list, leaving it empty.
30. **B) 1:** The `or` operator returns the first truthy value it encounters.
31. **B) [1, 2, 3]:** `a.copy()` creates a separate copy of the list, so modifications to `b` do not affect `a`.
32. **B) 3:** The `and` operator returns the last evaluated operand if all are truthy.
33. **A) True:** The string "hello" does indeed end with the character "o".
34. **A) True:** This is a chained comparison, equivalent to `(1 < 2) and (2 < 3)`, which is `True`.
35. **C) 3:** `pop()` without an argument removes and returns the last item of the list.
36. **A) True:** `0` is a "falsy" value, so `not 0` evaluates to `True`.
37. **B) -1:** `find` returns -1 when the substring is not found.
38. **B) False:** `is` checks for object identity. The integer `1` and the float `1.0` are different objects.
39. **A) [3, 2, 1]:** `reverse()` reverses the elements of the list in-place.
40. **B) 0:** The `and` operator returns the first falsy value it encounters.
