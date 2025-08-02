#a program to take input from user and store it in a file


# def main():
#     user_input = input("Enter some text: ")
#     with open("input.txt", "r+") as niket:
#         niket.write(user_input + '\n')
        
#     print("Input saved to 'input.txt'") 
#     with open("input.txt", "r") as file:
#         content = file.read()
#         print("Content of 'input.txt':")
#         print(content)


# a program to show pickling and unpickling and say we compare the time scale to read the same contents
# binary file and a normal text file

import pickle
import time
import os


def main():
    dictionary = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    # Pickling the dictionary
    start_time = time.time()
    with open('data.pkl', 'wb') as file:
        pickle.dump(dictionary, file)
    end_time = time.time()
    print(f"Pickling took {end_time - start_time:.6f} seconds.")
    # Unpickling the dictionary
    start_time = time.time()
    with open('data.pkl', 'rb') as file:
        loaded_dict = pickle.load(file)
        print("Unpickled dictionary:", loaded_dict)
    end_time = time.time()
    print(f"Unpickling took {end_time - start_time:.6f} seconds.")
    print("Loaded dictionary:", loaded_dict)
    # Reading a text file
    text_file_path = 'data.txt'
    with open(text_file_path, 'w') as file:
        file.write("This is a sample text file.\n")
    # Reading the text file
    start_time = time.time()
    with open(text_file_path, 'r') as file:
        content = file.read()
    end_time = time.time()
    print(f"Reading text file took {end_time - start_time:.6f} seconds.")
    print("Content of the text file:", content)
    # Clean up
    os.remove('data.pkl')
    os.remove(text_file_path)
    # Remove the created files
    print("Cleaned up created files.")
# This program demonstrates the use of pickling and unpickling in Python.

        
        
if __name__ == "__main__":
    main()