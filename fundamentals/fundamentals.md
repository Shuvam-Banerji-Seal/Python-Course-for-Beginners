# **A Beginner's Journey into Mathematical Python: Algorithms, Vectors, and Visualization**

## **Chapter 1: Introduction to Python for Mathematical Beginners**

Embarking on the path of computational mathematics requires a solid foundation in a programming language. Python, with its clear syntax and extensive libraries, serves as an excellent starting point for beginners interested in exploring mathematical algorithms and data manipulation. This chapter will guide you through the initial steps of setting up your Python environment, understanding fundamental Python syntax and data types, and introducing the core concepts of functional programming, a paradigm that aligns well with mathematical thinking.

### **1.1 Setting up the Python Environment**

The first step is to install Python on your system. It is recommended to use Python version 3.7 or later, as support for older versions has been discontinued.1 You can download the latest version of Python from the official Python website. Once installed, you will need a place to write and execute your Python code. Integrated Development Environments (IDEs) like PyCharm or Visual Studio Code provide a comprehensive environment for coding, with features such as code completion, debugging tools, and project management. Alternatively, simple text editors like Sublime Text or Atom can also be used for writing Python scripts, which can then be executed from the command line.  
For those interested in a more interactive and exploratory approach, especially beneficial for learning and experimenting with mathematical concepts, Jupyter notebooks and Google Colaboratory (Colab) offer convenient environments.1 Jupyter notebooks allow you to combine code, text, and visualizations in a single document, making it ideal for learning and sharing computational work. Colab, on the other hand, is a cloud-based Jupyter notebook environment that requires no setup and runs entirely in your web browser.1 This is particularly suited for machine learning and data analysis tasks, as it often provides access to powerful computing resources.  
As we progress through this course, we will be using external libraries that extend Python's capabilities for numerical computation and data visualization. The primary libraries we will need are NumPy and Matplotlib. NumPy (Numerical Python) is a fundamental library for scientific computing in Python, providing support for large, multi-dimensional arrays and a collection of high-level mathematical functions to operate on these arrays. Matplotlib is a comprehensive library for creating static, interactive, and animated visualizations in Python.4 These libraries can be easily installed using pip, Python's package installer. You can open your command prompt or terminal and run the following commands: pip install numpy matplotlib. This will download and install the necessary packages on your system, making them available for use in your Python projects.

### **1.2 Basic Python Syntax and Data Types**

Before diving into mathematical algorithms, it's essential to grasp the basic syntax and data types in Python. Python code is often described as being almost like pseudocode due to its readability and ability to express powerful ideas in a few lines.1 Python uses indentation to define code blocks, which is crucial for the structure and execution of your programs.  
Variables are used to store data, and they are assigned values using the equals sign (=). Python supports various operators for performing operations on these variables, including arithmetic operators (+, \-, \*, /, //, %, \*\*), comparison operators (==,\!=, \>, \<, \>=, \<=), and logical operators (and, or, not). Expressions are combinations of variables, operators, and values that result in a single value.  
Python has several built-in data types that you will encounter frequently. Integers (int) represent whole numbers, while floats (float) represent numbers with decimal points. Strings (str) are sequences of characters used to represent text, and booleans (bool) represent truth values (True or False).  
One of the fundamental data structures in Python is the list. A list is an ordered collection of items, which can be of different data types. Lists are defined by enclosing the items in square brackets \`\`, with items separated by commas. For example, my\_list \=. You can access individual elements in a list using their index, starting from 0 for the first element. For instance, my\_list would give you 1\. Basic operations on lists include finding their length using len(), adding elements using append(), and accessing a range of elements using slicing (e.g., my\_list\[1:3\] would give you \[2.5, "hello"\]).1 Lists will serve as our initial way to represent vectors.  
While lists are versatile, Python also offers other container types such as tuples, sets, and dictionaries.1 Tuples are similar to lists but are immutable, meaning their elements cannot be changed after creation. They are defined using parentheses (). Sets are unordered collections of unique elements, defined using curly braces {}. Dictionaries are collections of key-value pairs, also defined using curly braces {}, where each value is associated with a unique key. While our primary focus initially will be on lists, understanding these other container types provides a broader perspective on Python's capabilities.

### **1.3 Introduction to Functional Programming Concepts**

As we explore mathematical algorithms in Python, we will primarily adopt the functional programming paradigm. Functional programming is a style of programming where computation is treated as the evaluation of mathematical functions.6 It emphasizes the use of functions as the primary building blocks of programs. This approach can lead to code that is more modular, easier to understand, and less prone to side effects, which is particularly beneficial in the realm of mathematical computations.  
One of the core tenets of functional programming is the concept of **pure functions**. A pure function is a function that, given the same input, will always produce the same output, and it has no side effects.7 Side effects refer to any observable effect a function has on the state of the program outside of its return value, such as modifying global variables or printing to the console. For example, a function that takes a number and returns its square is a pure function, as it always produces the same square for the same input and does not alter any external state.7 This predictability makes pure functions easier to reason about and test.  
Another important concept is **immutability**. In functional programming, once a variable is initialized, its value should not be modified.7 Instead of changing the existing variable, new variables are created to hold the results of computations. This helps prevent unexpected changes to data and leads to more robust and maintainable code.  
**First-class functions** are a fundamental aspect of functional programming in Python.6 This means that functions in Python can be treated like any other object. You can assign a function to a variable, pass a function as an argument to another function, and return a function as the result of another function.6 For instance, you can define a function greet and then assign it to another variable say\_hello: say\_hello \= greet. Now, calling say\_hello() will have the same effect as calling greet().  
**Higher-order functions** are functions that operate on other functions.7 They can take functions as arguments or return functions as their results. A good example is the built-in sorted() function in Python.6 By default, if you pass a list of strings to sorted(), it sorts them alphabetically. However, sorted() also takes an optional key argument, which allows you to specify a callback function that will be used to determine the sorting order. For example, you can sort a list of strings by their length by passing the built-in len function as the key argument: sorted(animals, key=len).  
Understanding these core principles of functional programming early on will set the stage for implementing mathematical algorithms in a functional style. This approach emphasizes clarity and avoids side effects, which is particularly beneficial for beginners learning mathematical concepts through code. By introducing functional programming upfront, learners will be primed to think in terms of functions and data transformations, which aligns well with the mathematical nature of the algorithms to be covered.

## **Chapter 2: Exploring Fundamental Mathematical Algorithms in Python (Functional Approach)**

This chapter will delve into the implementation of several beginner-friendly mathematical algorithms using the functional programming concepts introduced in the previous chapter. We will explore Armstrong numbers, perfect numbers, and happy numbers, showcasing how these concepts can be elegantly expressed in Python using a functional approach.

### **2.1 Armstrong Numbers**

An Armstrong number (also known as a narcissistic number) is a number that is equal to the sum of its own digits each raised to the power of the number of digits.9 For example, 153 is a 3-digit Armstrong number because 13+53+33=1+125+27=153.9 Similarly, 1634 is a 4-digit Armstrong number since 14+64+34+44=1+1296+81+256=1634.9  
To implement a function that checks if a given number is an Armstrong number using a functional approach in Python, we can follow these steps:

1. Convert the input number to a string to easily access its individual digits.  
2. Determine the number of digits in the number (which will be the power to which each digit is raised).  
3. Convert each digit back to an integer.  
4. Raise each digit to the power of the total number of digits.  
5. Calculate the sum of these powers.  
6. Compare the sum with the original number. If they are equal, the number is an Armstrong number.

Here is a Python implementation of the is\_armstrong function using the map() function and anonymous (lambda) functions to achieve this in a functional style:

Python

def is\_armstrong(number):  
    num\_str \= str(number)  
    n \= len(num\_str)  
    digits \= map(int, list(num\_str))  
    powers \= map(lambda digit: digit \*\* n, digits)  
    return sum(powers) \== number

\# Example usage:  
print(is\_armstrong(153))   \# Output: True  
print(is\_armstrong(120))   \# Output: False  
print(is\_armstrong(1634))  \# Output: True

In this implementation, str(number) converts the input number to a string. len(num\_str) gets the number of digits. map(int, list(num\_str)) iterates through each character in the string, converts it to an integer, and returns an iterator of these integer digits. The second map() function applies an anonymous function lambda digit: digit \*\* n to each digit, raising it to the power of n. Finally, sum(powers) calculates the sum of these powers, and the function returns True if this sum is equal to the original number, and False otherwise. This approach avoids explicit loops and focuses on applying transformations to the digits using functional constructs.10

### **2.2 Perfect Numbers**

A perfect number is a positive integer that is equal to the sum of its proper divisors, excluding the number itself.12 For example, the proper divisors of 6 are 1, 2, and 3, and their sum is 1+2+3=6, so 6 is a perfect number.12 The proper divisors of 28 are 1, 2, 4, 7, and 14, and their sum is 1+2+4+7+14=28, making 28 another perfect number.16  
To check if a number is perfect using a functional approach, we need to:

1. Find all the proper divisors of the number (integers that divide the number evenly, excluding the number itself).  
2. Calculate the sum of these divisors.  
3. Compare the sum with the original number. If they are equal, the number is perfect.

Here's a Python implementation using the filter() function and a lambda function to find the divisors:

Python

def is\_perfect(number):  
    if number \< 1:  
        return False  
    divisors \= filter(lambda i: number % i \== 0, range(1, number))  
    return sum(divisors) \== number

\# Example usage:  
print(is\_perfect(6))    \# Output: True  
print(is\_perfect(28))   \# Output: True  
print(is\_perfect(12))   \# Output: False

In this code, range(1, number) generates a sequence of numbers from 1 up to (but not including) the input number. The filter() function then applies the lambda function lambda i: number % i \== 0 to each number in this range. This lambda function returns True if number is divisible by i (i.e., the remainder is 0), and False otherwise. Thus, filter() returns an iterator containing only the proper divisors of number. Finally, sum(divisors) calculates the sum of these divisors, and the function returns True if the sum is equal to the original number. This demonstrates the use of filter() for selecting elements based on a specific condition in a functional manner.13

### **2.3 Happy Numbers**

A happy number is a number that eventually reaches 1 when repeatedly replaced by the sum of the squares of its digits.22 If the process ends in a cycle that does not include 1, then the number is not a happy number. For example, starting with 19: 12+92=1+81=82; 82+22=64+4=68; 62+82=36+64=100; 12+02+02=1. Since we reached 1, 19 is a happy number.22  
To determine if a number is happy, we need to repeatedly apply the process of summing the squares of its digits until we either reach 1 or encounter a number we have seen before (indicating a cycle).  
Here is a Python implementation using a functional approach for calculating the sum of squares of digits and an iterative approach with a set for cycle detection:

Python

def next\_happy(number):  
    return sum(map(lambda digit: int(digit)\*\*2, str(number)))

def is\_happy(number):  
    seen \= set()  
    while number\!= 1 and number not in seen:  
        seen.add(number)  
        number \= next\_happy(number)  
    return number \== 1

\# Example usage:  
print(is\_happy(19))   \# Output: True  
print(is\_happy(4))    \# Output: False

The next\_happy function takes an integer, converts it to a string, then uses map() with a lambda function to square each digit (after converting it back to an integer). The sum() function then calculates the sum of these squares. The is\_happy function uses a while loop to repeatedly apply next\_happy to the input number. A set called seen is used to keep track of the numbers encountered during the process. If the number becomes 1, it's a happy number, and the function returns True. If the number is already in the seen set, it means we have entered a cycle that does not include 1, so the number is not happy, and the function returns False. While the core transformation of calculating the sum of squares of digits is done functionally, the overall process of iteration and cycle detection utilizes a more traditional imperative style for clarity.22

### **2.4 Additional Beginner-Friendly Mathematical Algorithms with Python Examples**

Beyond Armstrong, perfect, and happy numbers, there are several other mathematical algorithms suitable for beginners that can be implemented using Python, often leveraging functional programming concepts.  
**Palindrome Check:** A palindrome is a number or a sequence that reads the same forwards and backward. For a number, we can check if it's a palindrome by converting it to a string and comparing the string with its reverse. This can be done concisely using slicing:

Python

def is\_palindrome(number):  
    return str(number) \== str(number)\[::-1\]

print(is\_palindrome(121))   \# Output: True  
print(is\_palindrome(123))   \# Output: False

**Prime Number Check:** A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself. We can check if a number is prime by iterating from 2 up to the square root of the number and checking for divisibility.

Python

import math

def is\_prime(number):  
    if number \<= 1:  
        return False  
    if number \<= 3:  
        return True  
    if number % 2 \== 0 or number % 3 \== 0:  
        return False  
    for i in range(5, int(math.sqrt(number)) \+ 1, 6):  
        if number % i \== 0 or number % (i \+ 2\) \== 0:  
            return False  
    return True

print(is\_prime(17))   \# Output: True  
print(is\_prime(15))   \# Output: False

**Factorial Calculation:** The factorial of a non-negative integer n, denoted by n\!, is the product of all positive integers less than or equal to n. This can be elegantly calculated using the reduce() function from the functools module:

Python

from functools import reduce

def factorial(n):  
    if n \== 0:  
        return 1  
    return reduce(lambda x, y: x \* y, range(1, n \+ 1))

print(factorial(5))   \# Output: 120

**Fibonacci Sequence Generation:** The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, usually starting with 0 and 1\. A functional recursive approach can be used to generate Fibonacci numbers:

Python

def fibonacci(n):  
    if n \<= 1:  
        return n  
    else:  
        return fibonacci(n-1) \+ fibonacci(n-2)

print(fibonacci(10))  \# Output: 55

These examples illustrate how various simple mathematical algorithms can be implemented in Python, often utilizing functional programming principles for conciseness and clarity. Exploring these algorithms helps reinforce the understanding of basic programming constructs and their application in solving mathematical problems.

## **Chapter 3: Understanding Vectors in Python**

In mathematics, a vector is often described as an object that has both magnitude and direction. In a more computational context, particularly in data science and linear algebra, a vector can be thought of as a one-dimensional array of numbers. This chapter will explore how vectors can be represented using Python lists and discuss the limitations of this approach when dealing with numerical vector operations.

### **3.1 Representing Vectors using Python Lists**

Python lists provide a natural way to represent vectors. As an ordered collection of elements, a list can hold a sequence of numbers, which corresponds directly to the mathematical concept of a vector's components. For instance, a vector in a two-dimensional space, say with components 1 and 2, can be represented in Python as vector\_a \=. Similarly, a vector in three-dimensional space with components 1, 2, and 3 can be represented as vector\_b \=. Python's built-in range() function can also be used to create lists of numbers, which can then be used to represent vectors, for example, list(range(5)) creates a list \`\`.1  
Basic operations on these list-based vectors are straightforward using Python's list functionalities. You can access individual elements of a vector (list) using indexing. For vector\_b \=, vector\_b would give you the first component, which is 1\. The length of a vector, corresponding to the number of its components, can be found using the len() function. For vector\_b, len(vector\_b) would return 3\. Slicing can also be used to access a subset of the vector's components; for example, vector\_b\[1:3\] would give you a new list \`\` containing the second and third components.1

### **3.2 Limitations of Python Lists for Numerical Vector Operations**

While Python lists can represent vectors, they have several limitations when it comes to performing numerical operations efficiently, especially for large vectors.  
One significant issue is **performance**. Python is an interpreted language, and while lists are a fundamental data structure, operations on them, especially when involving loops, can be slower compared to optimized implementations in lower-level languages like C. Libraries such as NumPy are built on top of C, allowing for much faster execution of numerical computations.3 When dealing with large vectors, the performance difference between using Python lists and optimized libraries can be substantial.  
Another key limitation is the **lack of built-in support for element-wise mathematical operations**. If you have two vectors represented as Python lists, say list\_a \= and list\_b \=, and you want to add them element-wise to get \[1+4, 2+5, 3+6\] \=, you cannot simply use the \+ operator. In Python, adding two lists using \+ results in concatenation, i.e., list\_a \+ list\_b would give you \`\`. To perform element-wise addition using lists, you would typically need to iterate through the lists using a loop and perform the addition element by element, storing the results in a new list.25 This necessity for explicit looping not only makes the code more verbose but also less efficient. Similarly, other element-wise operations like subtraction, multiplication, and division would also require explicit loops.  
Furthermore, performing more **advanced vector operations** such as the dot product or cross product is not directly supported by Python lists. You would need to implement these operations yourself, again likely involving loops. For example, the dot product of two vectors \[a1​,a2​,a3​\] and \[b1​,b2​,b3​\] is a1​b1​+a2​b2​+a3​b3​. To calculate this using lists, you would need to iterate through the lists, multiply corresponding elements, and then sum up the results.  
Finally, Python lists can have a **higher memory overhead** compared to more specialized array structures when dealing with homogeneous numerical data.26 Because Python lists can store elements of different data types, they need to store additional type information for each element. When you have a large vector where all elements are of the same numerical type (e.g., all integers or all floats), this per-element overhead in lists can lead to less efficient memory usage compared to structures that are designed to store homogeneous data contiguously in memory.  
In summary, while Python lists can serve as a basic way to represent vectors, their limitations in performance for numerical computations, the lack of direct support for element-wise mathematical operations, the difficulty in performing advanced vector operations without explicit loops, and the potential for higher memory overhead make them less suitable for serious numerical work, especially when dealing with large datasets. These limitations motivate the need for a more specialized library like NumPy, which is designed specifically for efficient numerical operations on arrays and vectors.

## **Chapter 4: Leveraging NumPy for Efficient Vector Operations**

To overcome the limitations of Python lists for numerical vector operations, we turn to the NumPy library. NumPy (Numerical Python) is a cornerstone of scientific computing in Python.1 It provides support for large, multi-dimensional arrays and a vast collection of high-level mathematical functions that operate efficiently on these arrays.

### **4.1 Introduction to the NumPy Library and its ndarray Object**

NumPy is an open-source Python library widely used in science and engineering. It is the fundamental package for numerical computation in Python.26 NumPy's power comes from its core data structure, the **ndarray** (n-dimensional array) object.3 Unlike Python lists, NumPy arrays are typically homogeneous, meaning that all elements within an array must be of the same data type.2 This homogeneity allows NumPy to store and manipulate large datasets in a much more memory-efficient manner and enables faster operations. NumPy also supports vectorized operations, which means that mathematical functions can be applied to entire arrays at once, rather than element by element, leading to significant performance improvements.3  
To use NumPy in your Python code, you first need to import it. The standard convention is to import NumPy with the alias np: import numpy as np.27 This allows you to access NumPy's functions and objects using the prefix np..  
The ndarray is the central data structure in NumPy. It can represent vectors (1-dimensional arrays), matrices (2-dimensional arrays), or higher-dimensional tensors (N-dimensional arrays).27 The homogeneity of the ndarray is a key factor in its efficiency. All elements of an array must be of the same type, such as integers, floating-point numbers, or complex numbers.2 This allows NumPy to store the data in contiguous blocks of memory, which is much more efficient for both storage and computation compared to Python lists, where elements can be scattered in memory and have varying data types.26 Once created, the total size of a NumPy array cannot be changed, and for multi-dimensional arrays, the shape must be "rectangular," meaning each row must have the same number of columns.2

### **4.2 Creating and Manipulating NumPy Arrays**

You can create NumPy arrays from Python lists using the np.array() function.27 For example, to create a NumPy array representing the vector $$, you would write: numpy\_vector \= np.array(). NumPy will automatically infer the data type of the array based on the elements in the list.  
NumPy also provides several convenient functions for creating arrays with specific initial values or ranges :

* np.zeros(shape): Creates an array filled with zeros. The shape argument specifies the dimensions of the array (e.g., np.zeros(5) for a 1D array of 5 zeros, or np.zeros((2, 3)) for a 2D array of 2 rows and 3 columns).  
* np.ones(shape): Creates an array filled with ones, with the shape argument specifying the dimensions.  
* np.arange(start, stop, step): Creates an array with a range of elements, similar to Python's range() function but returns an ndarray. You can specify the start, stop (exclusive), and step size. For example, np.arange(0, 10, 2\) will create the array \`\`.  
* np.linspace(start, stop, num): Creates an array with values that are spaced linearly in a specified interval. You specify the start and end points (inclusive) and the number of evenly spaced values to generate. For example, np.linspace(0, 10, num=5) will create the array \[ 0\. , 2.5, 5\. , 7.5, 10\. \].

Once you have a NumPy array, you can inspect its properties using various attributes 27:

* ndim: Returns the number of dimensions of the array. A vector has ndim \= 1, a matrix has ndim \= 2, and so on.  
* shape: Returns a tuple indicating the number of elements along each dimension. For a vector of length 5, the shape would be (5,). For a 2x3 matrix, the shape would be (2, 3).  
* size: Returns the total number of elements in the array.  
* dtype: Returns the data type of the elements in the array (e.g., int64, float64).

You can access and modify elements in NumPy arrays using indexing and slicing, similar to Python lists.2 NumPy arrays are 0-indexed, meaning the first element is at index 0\. You can use slice notation (e.g., array\[1:4\]) to access a portion of the array. One important difference between slicing a list and slicing a NumPy array is that slicing an array returns a **view** of the original array, not a copy.27 This means that if you modify a slice of an array, the original array will also be changed.  
The shape of a NumPy array can be changed without altering its data using the .reshape() method.3 For example, if you have a 1D array with 6 elements, you can reshape it into a 2x3 matrix using array.reshape((2, 3)). The new shape must be compatible with the original number of elements.

### **4.3 Advantages of NumPy Arrays over Python Lists for Vectors**

NumPy arrays offer several significant advantages over Python lists when it comes to representing and operating on vectors, especially in the context of numerical computing.26  
One of the primary advantages is **memory efficiency**. NumPy arrays store elements in contiguous memory locations, and because all elements are of the same data type, there is no need to store type information for each element, reducing memory overhead and fragmentation.3 This is particularly beneficial when working with large vectors.  
**Speed** is another crucial advantage. NumPy operations, especially vectorized operations, are implemented in highly optimized C code.3 This means that operations performed on entire NumPy arrays are often significantly faster than equivalent operations performed element-wise in Python using loops. Vectorization allows you to express computations as operations on entire arrays, which NumPy can then execute very efficiently. For instance, adding two NumPy arrays of the same shape is as simple as array1 \+ array2, and this operation is performed element-wise in a highly optimized way.25  
NumPy also supports **broadcasting**, a powerful feature that allows you to perform operations between arrays of different shapes under certain conditions without the need for explicit looping.3 This can simplify your code and make it more efficient when, for example, you want to add a scalar to a vector or perform operations between arrays with compatible dimensions.  
Furthermore, NumPy comes with an **extensive library of built-in mathematical functions** that operate directly on NumPy arrays.3 These include functions for basic arithmetic, linear algebra, statistics, Fourier transforms, and more. For example, you can calculate the sine of all elements in a NumPy array using np.sin(array).32 For linear algebra operations, NumPy provides functions for dot products (np.dot()), matrix multiplication, finding determinants, inverses, eigenvalues, and eigenvectors.3

### **4.4 Element-wise Operations and Vector Arithmetic with NumPy**

Performing element-wise operations and vector arithmetic with NumPy arrays is straightforward and efficient.3 If you have two NumPy arrays of the same shape, you can perform basic arithmetic operations like addition (+), subtraction (-), multiplication (\*), and division (/) directly between them. These operations will be applied element-wise, resulting in a new NumPy array with the results.25  
For example, if you have vector\_x \= np.array() and vector\_y \= np.array(), then vector\_x \+ vector\_y will result in np.array(). Similarly, vector\_x \* vector\_y will give you np.array().  
The **dot product** of two vectors is a fundamental operation in linear algebra. In NumPy, you can calculate the dot product of two 1D arrays (vectors) using the np.dot() function or the @ operator (available in Python 3.5 and later).3 For example, np.dot(vector\_x, vector\_y) or vector\_x @ vector\_y will compute (1×4)+(2×5)+(3×6)=4+10+18=32.  
Other common vector operations, such as scalar multiplication (multiplying a vector by a single number) and vector addition/subtraction, are also easily performed with NumPy. For instance, 3 \* vector\_x will result in np.array().  
In conclusion, NumPy arrays provide a significantly more efficient and convenient way to perform numerical vector operations in Python due to their homogeneous nature, vectorized implementations, and rich set of built-in functions. This makes them indispensable for scientific computing and data analysis.

## **Chapter 5: Deep Dive into Functional Programming in Python**

In Chapter 1, we introduced the fundamental concepts of functional programming. Now, we will delve deeper into these principles and explore how they can be applied to solve mathematical problems and work with vectors in Python, often in conjunction with the efficiency of NumPy.

### **5.1 Core Principles of Functional Programming (Recap and Expansion)**

Let's revisit the core principles of functional programming with a more in-depth look.6  
**Pure Functions:** As discussed earlier, pure functions are deterministic; they always return the same output for the same input and have no side effects.7 This predictability makes code easier to understand, test, and debug. For example, a function that calculates the square of a number is pure.  
**Immutability:** In functional programming, data structures are generally treated as immutable. Once created, their state cannot be changed. Operations on immutable data structures typically return new data structures rather than modifying the original.7 This helps in managing state and avoiding unexpected modifications. While Python lists are mutable, tuples are an example of an immutable sequence type. NumPy arrays, although mutable, can often be treated as immutable in a functional style by performing operations that create new arrays.  
**First-Class Functions:** Python treats functions as first-class citizens, meaning they can be assigned to variables, passed as arguments to other functions, and returned from functions.6 This allows for powerful programming patterns where behavior can be treated as data.  
**Higher-Order Functions:** These are functions that operate on other functions, either by taking them as arguments or by returning them.7 Examples in Python include map(), filter(), and sorted(). Decorators in Python also leverage higher-order functions to modify or enhance other functions.35  
The benefits of adhering to functional programming principles include increased code clarity, as pure functions are easier to reason about; improved testability, as the output of a pure function depends solely on its input; and potential for easier parallelization, as the lack of shared mutable state reduces the risk of concurrency issues.6

### **5.2 Applying Functional Programming Concepts to Solve Mathematical Problems and Vector Operations**

We have already seen examples of applying functional programming to solve mathematical problems in Chapter 2 with Armstrong, perfect, and happy numbers. These examples utilized map() and filter() to process sequences of numbers in a declarative way, focusing on what needs to be done rather than explicitly how to do it with loops.  
When it comes to vector operations, while NumPy's strength lies in its efficient vectorized operations that are inherently functional in their application to entire arrays, functional programming concepts can still be valuable. For instance, you might use map() to apply a specific function to each element of a NumPy array or filter() to select elements based on a certain condition.  
Consider calculating the magnitude (or Euclidean norm) of a vector. If we have a NumPy array representing a vector, we can use a functional approach to first square each element and then sum the squares before taking the square root:

Python

import numpy as np  
from functools import reduce

def square(x):  
    return x \*\* 2

vector \= np.array()  
squared\_elements \= map(square, vector)  
sum\_of\_squares \= reduce(lambda a, b: a \+ b, squared\_elements)  
magnitude \= np.sqrt(sum\_of\_squares)  
print(magnitude)  \# Output: 3.7416573867739413

In this example, map(square, vector) applies the square function to each element of the vector, and reduce(lambda a, b: a \+ b, squared\_elements) sums up the squared elements. Finally, np.sqrt() calculates the square root. While NumPy has a built-in function np.linalg.norm() to achieve this more directly and efficiently, this example illustrates how functional programming concepts can be used with NumPy.

### **5.3 Using map(), filter(), and reduce() in Python**

The functions map(), filter(), and reduce() are fundamental tools in Python for functional programming.6  
**map():** The map() function takes a function and an iterable (like a list or a NumPy array) as arguments and applies the function to each item of the iterable, returning an iterator of the results.6 The syntax is map(function, iterable,...). If the function takes multiple arguments, you can provide multiple iterable arguments to map(), and the function will be called with the corresponding elements from each iterable. For example, map(int, \["1", "2", "3"\]) will convert each string in the list to an integer, resulting in an iterator that yields 1, 2, 3\.8  
**filter():** The filter() function also takes a function and an iterable as arguments. It applies the function to each element of the iterable and returns an iterator containing only the elements for which the function returns a truthy value (i.e., True or a non-zero/non-empty value).6 The syntax is filter(function, iterable). For example, filter(lambda x: x % 2 \== 0, range(10)) will filter the numbers from 0 to 9 and return an iterator containing only the even numbers: 0, 2, 4, 6, 8\.7  
**reduce():** The reduce() function is available in the functools module and applies a function of two arguments cumulatively to the items of an iterable, from left to right, so as to reduce the iterable to a single value.6 The syntax is reduce(function, iterable\[, initializer\]). The function is called with the first two items of the iterable, then with the result of that call and the next item, and so on. If an optional initializer is provided, it is used as the first argument to the first call of the function along with the first element of the iterable. For example, reduce(lambda x, y: x \+ y, ) will calculate the sum of the numbers in the list: ((((1+2)+3)+4)+5)=15.6  
While map(), filter(), and reduce() are powerful tools for functional programming, Python also offers more Pythonic alternatives in many cases, such as **list comprehensions** and **generator expressions**.6 For example, squaring each element in a list can be done using map(lambda x: x\*\*2, numbers) or more concisely with a list comprehension: \[x\*\*2 for x in numbers\]. Similarly, filtering even numbers can be done with filter(lambda x: x % 2 \== 0, numbers) or \[x for x in numbers if x % 2 \== 0\]. These alternatives often provide better readability for common operations.  
In summary, while NumPy provides highly optimized functions for vector operations, understanding and applying functional programming principles can still be valuable for structuring code, especially for pre- and post-processing data or for implementing certain types of algorithms. The functions map(), filter(), and reduce() are key tools in the functional programming toolkit in Python, although list comprehensions and generator expressions often offer more concise and readable solutions for many common tasks.

## **Chapter 6: Practical Python Programs and Examples**

This chapter will provide a collection of small Python programs that demonstrate the concepts we have learned in the previous chapters. These examples will cover mathematical algorithms, vector operations using both Python lists and NumPy arrays, and the application of functional programming concepts.  
**1\. Checking for Armstrong Numbers (Functional Approach):**

Python

def is\_armstrong(number):  
    num\_str \= str(number)  
    n \= len(num\_str)  
    digits \= map(int, list(num\_str))  
    powers \= map(lambda digit: digit \*\* n, digits)  
    return sum(powers) \== number

print(f"Is 153 an Armstrong number? {is\_armstrong(153)}")  
print(f"Is 120 an Armstrong number? {is\_armstrong(120)}")

**2\. Checking for Perfect Numbers (Functional Approach):**

Python

def is\_perfect(number):  
    if number \< 1:  
        return False  
    divisors \= filter(lambda i: number % i \== 0, range(1, number))  
    return sum(divisors) \== number

print(f"Is 6 a perfect number? {is\_perfect(6)}")  
print(f"Is 28 a perfect number? {is\_perfect(28)}")  
print(f"Is 12 a perfect number? {is\_perfect(12)}")

**3\. Checking for Happy Numbers:**

Python

def next\_happy(number):  
    return sum(map(lambda digit: int(digit)\*\*2, str(number)))

def is\_happy(number):  
    seen \= set()  
    while number\!= 1 and number not in seen:  
        seen.add(number)  
        number \= next\_happy(number)  
    return number \== 1

print(f"Is 19 a happy number? {is\_happy(19)}")  
print(f"Is 4 a happy number? {is\_happy(4)}")

**4\. Basic Vector Operations using Python Lists (Highlighting Limitations):**

Python

def add\_lists(list1, list2):  
    if len(list1)\!= len(list2):  
        raise ValueError("Lists must have the same length for element-wise addition.")  
    result \=  
    for i in range(len(list1)):  
        result.append(list1\[i\] \+ list2\[i\])  
    return result

list\_a \=   
list\_b \=   
print(f"Element-wise addition of {list\_a} and {list\_b}: {add\_lists(list\_a, list\_b)}")

\# Attempting direct addition (concatenation):  
print(f"Direct addition of {list\_a} and {list\_b}: {list\_a \+ list\_b}")

**5\. Basic Vector Operations using NumPy Arrays:**

Python

import numpy as np

numpy\_a \= np.array()  
numpy\_b \= np.array()

print(f"Element-wise addition of {numpy\_a} and {numpy\_b}: {numpy\_a \+ numpy\_b}")  
print(f"Element-wise multiplication of {numpy\_a} and {numpy\_b}: {numpy\_a \* numpy\_b}")  
print(f"Dot product of {numpy\_a} and {numpy\_b}: {np.dot(numpy\_a, numpy\_b)}")  
print(f"Scalar multiplication of {numpy\_a} by 3: {3 \* numpy\_a}")

**6\. Using map() to Square Elements of a NumPy Array:**

Python

import numpy as np

numbers \= np.array()  
squared\_numbers \= list(map(lambda x: x \*\* 2, numbers))  
print(f"Squared numbers using map(): {squared\_numbers}")

**7\. Using filter() to Find Even Numbers in a Range:**

Python

even\_numbers \= list(filter(lambda x: x % 2 \== 0, range(10)))  
print(f"Even numbers from 0 to 9 using filter(): {even\_numbers}")

**8\. Using reduce() to Calculate the Product of a List:**

Python

from functools import reduce

numbers \=   
product \= reduce(lambda x, y: x \* y, numbers)  
print(f"Product of numbers using reduce(): {product}")

**9\. Calculating the Magnitude of a Vector using NumPy and Functional Programming:**

Python

import numpy as np  
from functools import reduce

def square(x):  
    return x \*\* 2

vector \= np.array()  
squared\_elements \= map(square, vector)  
sum\_of\_squares \= reduce(lambda a, b: a \+ b, squared\_elements)  
magnitude \= np.sqrt(sum\_of\_squares)  
print(f"Magnitude of vector {vector}: {magnitude}")

These practical examples illustrate how the concepts of mathematical algorithms, vector operations with lists and NumPy, and functional programming can be applied in Python. By experimenting with these examples, you can further solidify your understanding of these fundamental concepts.

## **Chapter 7: Data Visualization with Matplotlib**

Data visualization is a crucial aspect of understanding and communicating insights from data. Matplotlib is a powerful and widely-used Python library for creating static, interactive, and animated visualizations.4 It provides a flexible framework for generating various types of plots and charts.

### **7.1 Introduction to the Matplotlib Library**

Matplotlib is a comprehensive library for creating plots in Python.4 It is built on top of NumPy, making it efficient for handling large datasets.5 Matplotlib offers a module called pyplot, which provides a MATLAB-like interface for creating plots and charts, simplifying the process of generating various types of visualizations.5 To use Matplotlib, you typically import the pyplot module using the convention import matplotlib.pyplot as plt.5  
The fundamental building blocks of Matplotlib plots are **Figures** and **Axes**.5 A **Figure** can be thought of as the overall window or page on which everything is drawn. It can contain one or more **Axes** objects. An **Axes** object is where the actual plotting happens. It represents a single plot and contains the data, axes (x and y), title, labels, and other elements of the visualization. You can have multiple Axes within a single Figure, allowing you to create subplots or more complex layouts.

### **7.2 Plotting Basic Graphs: Line Plots and Scatter Plots**

Two of the most common types of graphs are line plots and scatter plots, and Matplotlib makes it easy to create them using the pyplot module.5  
**Line Plots:** Line plots are used to visualize the relationship between two continuous variables, often showing trends over time or across a range of values. You can create a line plot using the plt.plot() function. This function takes at least two arguments: the data for the x-axis and the data for the y-axis. For example, to plot the function y=x2 for values of x from \-5 to 5, you could do the following:

Python

import matplotlib.pyplot as plt  
import numpy as np

x \= np.linspace(-5, 5, 100\)  \# Create an array of 100 evenly spaced values from \-5 to 5  
y \= x \*\* 2

plt.plot(x, y)  
plt.show()

This will display a line plot of the parabola y=x2. You can also plot multiple lines on the same graph by calling plt.plot() multiple times before calling plt.show().38  
**Scatter Plots:** Scatter plots are used to visualize the relationship between two variables, where each point on the plot represents a pair of values. They are useful for identifying patterns, correlations, or clusters in the data. You can create a scatter plot using the plt.scatter() function, which also takes the x and y data as arguments. For example, to plot 50 random data points:

Python

import matplotlib.pyplot as plt  
import numpy as np

x \= np.random.rand(50)  
y \= np.random.rand(50)

plt.scatter(x, y)  
plt.show()

This will display a scatter plot with 50 randomly positioned points.

### **7.3 Customizing Plots: Labels, Titles, Legends, and Styles**

Matplotlib provides extensive options for customizing the appearance of your plots to make them more informative and visually appealing.5  
You can add a title to your plot using the plt.title() function, and you can add labels to the x and y axes using plt.xlabel() and plt.ylabel() respectively. For example:

Python

plt.plot(x, y)  
plt.title("Parabola y \= x^2")  
plt.xlabel("x-axis")  
plt.ylabel("y-axis")  
plt.show()

If you have multiple plots on the same axes, you can add a legend to identify them using the plt.legend() function. To do this, you need to provide a label argument to the plt.plot() or plt.scatter() function for each plot, and then call plt.legend():

Python

plt.plot(x, y, label="y \= x^2")  
plt.plot(x, \-y, label="y \= \-x^2")  
plt.xlabel("x-axis")  
plt.ylabel("y-axis")  
plt.title("Parabola and its reflection")  
plt.legend()  
plt.show()

You can also customize the style of the lines and markers in your plots by using additional arguments in the plotting functions.5 For example, you can change the color of a line using the color argument, the width using linewidth, and the style using linestyle. For scatter plots, you can change the marker style using marker and the size using s.

Python

plt.plot(x, y, color='red', linewidth=2, linestyle='--', label="y \= x^2")  
plt.scatter(x, \-y, color='blue', marker='o', s=20, label="y \= \-x^2")  
plt.xlabel("x-axis")  
plt.ylabel("y-axis")  
plt.title("Customized Plots")  
plt.legend()  
plt.show()

Finally, to display your plot, you need to call the plt.show() function. This will open a window showing the generated visualization.  
Introducing basic plotting with Matplotlib allows you to visualize data, including the output of mathematical algorithms and vector data, which can provide a more intuitive understanding of the concepts. Matplotlib is a fundamental library for data visualization in Python, offering a wide range of plot types and customization options to effectively represent your data.

## **Chapter 8: Understanding Shallow and Deep Copy in Python**

When working with objects in Python, it's important to understand how copying objects works, especially when dealing with mutable data structures like lists and NumPy arrays. Python provides two main ways to copy objects: shallow copy and deep copy.

### **8.1 The Concept of Object References in Python**

In Python, variables do not directly store values. Instead, they store references to objects in memory.39 When you assign one variable to another (e.g., a \= b), you are essentially making both variables refer to the same object. This means that if the object is mutable, changes made through one variable will be reflected when accessing the object through the other variable.40  
Python has two main categories of objects: mutable and immutable.40 **Immutable objects** are those whose state cannot be changed after they are created. Examples include numbers (integers, floats), strings, and tuples. When you perform an operation that seems to modify an immutable object, you are actually creating a new object with the modified value. **Mutable objects**, on the other hand, can be changed after they are created. Examples include lists, dictionaries, and sets.  
Understanding this concept of object references is crucial for comprehending how copying works in Python. When you copy an object, you might want to create a new object that is independent of the original, or you might just need a new reference to the same object. This distinction leads to the concepts of shallow and deep copy.

### **8.2 Shallow Copy: Creating New Objects with Shared References**

A **shallow copy** creates a new compound object (like a list or a dictionary) and then, to the extent possible, inserts references into it to the objects found in the original.39 In other words, the new object is a copy of the original object's structure, but the elements within the new object are still the same objects as the elements in the original object.  
There are several ways to create shallow copies in Python 39:

* **Using the copy() method:** For lists and dictionaries, you can use the built-in copy() method to create a shallow copy. For example, new\_list \= original\_list.copy() and new\_dict \= original\_dict.copy().  
* **Using list slicing:** For lists, you can also create a shallow copy using slicing with \[:\]. For example, new\_list \= original\_list\[:\].  
* **Using copy.copy():** The copy module provides a copy() function that can be used to create a shallow copy of most compound objects. You need to import the module first: import copy, and then use new\_object \= copy.copy(original\_object).

Let's see an example with lists:

Python

original\_list \= \]  
shallow\_copied\_list \= original\_list.copy()

\# Modify an element in the shallow copy (top-level)  
shallow\_copied\_list \= 99  
print(f"Original list after modifying shallow copy (top-level): {original\_list}")  
print(f"Shallow copied list after modification (top-level): {shallow\_copied\_list}")

\# Modify a nested element in the shallow copy  
shallow\_copied\_list \= 99  
print(f"Original list after modifying shallow copy (nested): {original\_list}")  
print(f"Shallow copied list after modification (nested): {shallow\_copied\_list}")

Output:

Original list after modifying shallow copy (top-level): \]  
Shallow copied list after modification (top-level): \]  
Original list after modifying shallow copy (nested): \]  
Shallow copied list after modification (nested): \]

As you can see, when we modified the first element (a top-level element) of the shallow\_copied\_list, the original\_list was not affected. However, when we modified an element within the nested list, the change was reflected in both shallow\_copied\_list and original\_list. This is because the shallow copy only created a new list object, but the nested list \`\` is still the same object in memory, and both lists hold a reference to it.42

### **8.3 Deep Copy: Creating Completely Independent Copies**

A **deep copy** constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.39 This means that if the original object contains other objects (like lists within a list), the deep copy will create new copies of those inner objects as well, ensuring that the copied object is entirely independent of the original.  
To create a deep copy in Python, you use the deepcopy() function from the copy module.39

Python

import copy

original\_list \= \]  
deep\_copied\_list \= copy.deepcopy(original\_list)

\# Modify an element in the deep copy (top-level)  
deep\_copied\_list \= 99  
print(f"Original list after modifying deep copy (top-level): {original\_list}")  
print(f"Deep copied list after modification (top-level): {deep\_copied\_list}")

\# Modify a nested element in the deep copy  
deep\_copied\_list \= 99  
print(f"Original list after modifying deep copy (nested): {original\_list}")  
print(f"Deep copied list after modification (nested): {deep\_copied\_list}")

Output:

Original list after modifying deep copy (top-level): \]  
Deep copied list after modification (top-level): \]  
Original list after modifying deep copy (nested): \]  
Deep copied list after modification (nested): \]

In this case, when we modified both the top-level and the nested elements of the deep\_copied\_list, the original\_list remained unchanged. This is becausecopy.deepcopy()\` created entirely new objects for both the outer list and the inner list, making them completely independent.42  
**Relevance to lists and NumPy arrays:** As we saw, slicing Python lists creates a shallow copy. For NumPy arrays, slicing also creates a **view**, which is similar to a shallow copy in that it refers to the same underlying data.27 If you need an independent copy of a NumPy array, you should use the .copy() method, which creates a new array with a copy of the data. For nested structures within NumPy arrays (though less common due to their homogeneous nature), copy.deepcopy() would still be relevant if complete independence is required.  
Understanding shallow and deep copy is crucial for avoiding unintended side effects when working with mutable data structures in Python, such as lists and NumPy arrays. Choosing the appropriate type of copy depends on whether you need independent copies of the data or shared references.

## **Conclusion**

This course has provided a foundational journey into the world of mathematical Python for beginners. We began by setting up the necessary environment and understanding the basic syntax and data types in Python, along with an introduction to the principles of functional programming. We then explored several fundamental mathematical algorithms, including Armstrong, perfect, and happy numbers, implementing them using a functional approach to emphasize clarity and avoid side effects.  
We delved into the concept of vectors, first using Python lists as a familiar way to represent them, and then highlighted the limitations of lists for numerical operations, particularly in terms of performance and the lack of built-in mathematical support. This led us to the NumPy library, where we discovered the power and efficiency of NumPy arrays for handling vector operations. The homogeneous nature of NumPy arrays, along with their vectorized operations and extensive mathematical function library, makes them indispensable for scientific computing in Python.  
We further explored the paradigm of functional programming, revisiting its core principles and demonstrating how it can be applied to solve mathematical problems and work with vectors, often complementing the efficiency of NumPy. We examined the use of map(), filter(), and reduce(), along with their more Pythonic alternatives like list comprehensions.  
To solidify the learning, we included a chapter with practical Python programs illustrating the concepts covered throughout the course. These examples ranged from checking mathematical properties of numbers to performing basic vector operations with both lists and NumPy arrays, and applying functional programming techniques.  
We then ventured into the realm of data visualization with Matplotlib, learning how to create basic line plots and scatter plots, and how to customize them with titles, labels, legends, and styles. This introduction to Matplotlib provides a crucial skill for visualizing data and the results of mathematical computations.  
Finally, we addressed the important topic of shallow and deep copy in Python, explaining the concept of object references and the differences between creating new objects with shared references (shallow copy) versus creating completely independent copies (deep copy). Understanding these concepts is essential for managing mutable data structures like lists and NumPy arrays effectively and avoiding unintended side effects in your code.  
By mastering the concepts and techniques presented in this course, you will have built a strong foundation for further exploration into more advanced mathematical algorithms, data analysis, and scientific computing with Python. The combination of functional programming principles and the power of libraries like NumPy and Matplotlib will equip you to tackle a wide range of computational challenges.

#### **Works cited**

1. Python Numpy Tutorial (with Jupyter and Colab), accessed on May 11, 2025, [https://cs231n.github.io/python-numpy-tutorial/](https://cs231n.github.io/python-numpy-tutorial/)  
2. the absolute basics for beginners — NumPy v2.2 Manual, accessed on May 11, 2025, [https://numpy.org/doc/2.2/user/absolute\_beginners.html](https://numpy.org/doc/2.2/user/absolute_beginners.html)  
3. NumPy Tutorial – Python Library | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/numpy-tutorial/](https://www.geeksforgeeks.org/numpy-tutorial/)  
4. Matplotlib — Visualization with Python, accessed on May 11, 2025, [https://matplotlib.org/](https://matplotlib.org/)  
5. Data Visualization using Matplotlib in Python \- GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/data-visualization-using-matplotlib/](https://www.geeksforgeeks.org/data-visualization-using-matplotlib/)  
6. Functional Programming in Python: When and How to Use It – Real ..., accessed on May 11, 2025, [https://realpython.com/python-functional-programming/](https://realpython.com/python-functional-programming/)  
7. Functional Programming in Python | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/functional-programming-in-python/](https://www.geeksforgeeks.org/functional-programming-in-python/)  
8. Functional Programming Tutorials & Notes | Python \- HackerEarth, accessed on May 11, 2025, [https://www.hackerearth.com/practice/python/functional-programming/functional-programming-1/tutorial/](https://www.hackerearth.com/practice/python/functional-programming/functional-programming-1/tutorial/)  
9. Armstrong Number in Python: An Overview With Examples \- upGrad, accessed on May 11, 2025, [https://www.upgrad.com/tutorials/software-engineering/python-tutorial/armstrong-number-in-python/](https://www.upgrad.com/tutorials/software-engineering/python-tutorial/armstrong-number-in-python/)  
10. Python Program to Check Armstrong Number | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/python-program-to-check-armstrong-number/](https://www.geeksforgeeks.org/python-program-to-check-armstrong-number/)  
11. Armstrong Number In Python \- Analytics Vidhya, accessed on May 11, 2025, [https://www.analyticsvidhya.com/blog/2024/06/armstrong-number-in-python/](https://www.analyticsvidhya.com/blog/2024/06/armstrong-number-in-python/)  
12. Perfect Number in Python: A Comprehensive Guide \- NxtWave, accessed on May 11, 2025, [https://www.ccbp.in/blog/articles/perfect-number-in-python](https://www.ccbp.in/blog/articles/perfect-number-in-python)  
13. Perfect Number in Python (5 Programs With Output) \- WsCube Tech, accessed on May 11, 2025, [https://www.wscubetech.com/resources/python/programs/perfect-number](https://www.wscubetech.com/resources/python/programs/perfect-number)  
14. Perfect Number in Python: Unraveling the Secrets of Number Theory \- upGrad, accessed on May 11, 2025, [https://www.upgrad.com/tutorials/software-engineering/python-tutorial/perfect-number-in-python/](https://www.upgrad.com/tutorials/software-engineering/python-tutorial/perfect-number-in-python/)  
15. Perfect Number in Python \- Scaler Topics, accessed on May 11, 2025, [https://www.scaler.com/topics/perfect-number-in-python/](https://www.scaler.com/topics/perfect-number-in-python/)  
16. Perfect Number Program in Python | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/perfect-number-program-in-python/](https://www.geeksforgeeks.org/perfect-number-program-in-python/)  
17. Perfect Number Program in Python \- Sanfoundry, accessed on May 11, 2025, [https://www.sanfoundry.com/python-program-check-perfect-number/](https://www.sanfoundry.com/python-program-check-perfect-number/)  
18. Perfect Number in Python | PrepInsta, accessed on May 11, 2025, [https://prepinsta.com/python-program/perfect-number-code/](https://prepinsta.com/python-program/perfect-number-code/)  
19. Perfect Number | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/perfect-number/](https://www.geeksforgeeks.org/perfect-number/)  
20. Creating a function that checks perfect numbers python \- Stack Overflow, accessed on May 11, 2025, [https://stackoverflow.com/questions/69771093/creating-a-function-that-checks-perfect-numbers-python](https://stackoverflow.com/questions/69771093/creating-a-function-that-checks-perfect-numbers-python)  
21. How can I improve this program in python to find out perfect numbers? \- Reddit, accessed on May 11, 2025, [https://www.reddit.com/r/learnpython/comments/1ddia6b/how\_can\_i\_improve\_this\_program\_in\_python\_to\_find/](https://www.reddit.com/r/learnpython/comments/1ddia6b/how_can_i_improve_this_program_in_python_to_find/)  
22. 202\. Happy Number \- In-Depth Explanation \- AlgoMonster, accessed on May 11, 2025, [https://algo.monster/liteproblems/202](https://algo.monster/liteproblems/202)  
23. Python Tutorials \- Happy Numbers \- YouTube, accessed on May 11, 2025, [https://www.youtube.com/watch?v=tNOYnyPnSlk](https://www.youtube.com/watch?v=tNOYnyPnSlk)  
24. Happy Numbers | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/happy-numbers/](https://www.geeksforgeeks.org/happy-numbers/)  
25. Python: Differences between lists and numpy array of objects \- Stack Overflow, accessed on May 11, 2025, [https://stackoverflow.com/questions/15944171/python-differences-between-lists-and-numpy-array-of-objects](https://stackoverflow.com/questions/15944171/python-differences-between-lists-and-numpy-array-of-objects)  
26. Python Lists VS Numpy Arrays | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/python-lists-vs-numpy-arrays/](https://www.geeksforgeeks.org/python-lists-vs-numpy-arrays/)  
27. the absolute basics for beginners — NumPy v2.2 Manual \- NumPy, accessed on May 11, 2025, [https://numpy.org/doc/stable/user/absolute\_beginners.html](https://numpy.org/doc/stable/user/absolute_beginners.html)  
28. physics.nyu.edu, accessed on May 11, 2025, [https://physics.nyu.edu/pine/pymanual/html/chap3/chap3\_arrays.html\#:\~:text=The%20elements%20of%20a%20NumPy,by%2Delement%20addition%20and%20multiplication.](https://physics.nyu.edu/pine/pymanual/html/chap3/chap3_arrays.html#:~:text=The%20elements%20of%20a%20NumPy,by%2Delement%20addition%20and%20multiplication.)  
29. 3\. Strings, Lists, Arrays, and Dictionaries — PyMan 0.9.31 documentation, accessed on May 11, 2025, [https://physics.nyu.edu/pine/pymanual/html/chap3/chap3\_arrays.html](https://physics.nyu.edu/pine/pymanual/html/chap3/chap3_arrays.html)  
30. NumPy Array vs Python List \- YouTube, accessed on May 11, 2025, [https://www.youtube.com/watch?v=6tAtbl0\_E4s](https://www.youtube.com/watch?v=6tAtbl0_E4s)  
31. Python Programming for Beginners \- Module 5A \- Math and NumPy \- YouTube, accessed on May 11, 2025, [https://www.youtube.com/watch?v=NQp6n0AcvEM](https://www.youtube.com/watch?v=NQp6n0AcvEM)  
32. NumPy Tutorial : Numpy Full Course \- YouTube, accessed on May 11, 2025, [https://m.youtube.com/watch?v=8Y0qQEh7dJg\&t=0s](https://m.youtube.com/watch?v=8Y0qQEh7dJg&t=0s)  
33. NumPy Crash Course \- Complete Tutorial \- YouTube, accessed on May 11, 2025, [https://www.youtube.com/watch?v=9JUAPgtkKpI](https://www.youtube.com/watch?v=9JUAPgtkKpI)  
34. 6\. Functional Programming — Python Practice Book 0.3 documentation \- Anand Chitipothu, accessed on May 11, 2025, [https://anandology.com/python-practice-book/functional-programming.html](https://anandology.com/python-practice-book/functional-programming.html)  
35. Learn Functional Programming in Python \[Full Course\] \- Boot.dev, accessed on May 11, 2025, [https://www.boot.dev/courses/learn-functional-programming-python](https://www.boot.dev/courses/learn-functional-programming-python)  
36. Python Data Visualization Course: Matplotlib, Seaborn, Plotly & Dash, accessed on May 11, 2025, [https://training.talkpython.fm/courses/python-data-visualization](https://training.talkpython.fm/courses/python-data-visualization)  
37. Data Visualization with Python | Coursera, accessed on May 11, 2025, [https://www.coursera.org/learn/python-for-data-visualization](https://www.coursera.org/learn/python-for-data-visualization)  
38. Python & Matplotlib: Getting Started with Matplotlib for Data ... \- Skillsoft, accessed on May 11, 2025, [https://www.skillsoft.com/course/python-matplotlib-getting-started-with-matplotlib-for-data-visualization-264357aa-1927-4f19-9e68-584ab074e4e8](https://www.skillsoft.com/course/python-matplotlib-getting-started-with-matplotlib-for-data-visualization-264357aa-1927-4f19-9e68-584ab074e4e8)  
39. copy — Shallow and deep copy operations — Python 3.13.3 documentation, accessed on May 11, 2025, [https://docs.python.org/3/library/copy.html](https://docs.python.org/3/library/copy.html)  
40. How to Copy Objects in Python: Shallow vs Deep Copy Explained ..., accessed on May 11, 2025, [https://realpython.com/copying-python-objects/](https://realpython.com/copying-python-objects/)  
41. docs.python.org, accessed on May 11, 2025, [https://docs.python.org/3/library/copy.html\#:\~:text=A%20shallow%20copy%20constructs%20a,objects%20found%20in%20the%20original.](https://docs.python.org/3/library/copy.html#:~:text=A%20shallow%20copy%20constructs%20a,objects%20found%20in%20the%20original.)  
42. Deep Copy and Shallow Copy in Python | GeeksforGeeks, accessed on May 11, 2025, [https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/](https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/)  
43. Python Copy List: What You Should Know \- DataCamp, accessed on May 11, 2025, [https://www.datacamp.com/tutorial/python-copy-list](https://www.datacamp.com/tutorial/python-copy-list)