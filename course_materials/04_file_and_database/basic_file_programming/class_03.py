# python code to show how fseek works in python
import os
import time
# Create a sample text file
with open('sample.txt', 'w') as file:
    for i in range(100):
        file.write(f"This is line {i}\n")

# Function to read a file using fseek
def read_file_with_fseek(file_path):
    """
    Reads and prints the content of a file starting from the beginning using fseek.

    Parameters:
    file_path (str): The path to the file to be read.

    This function opens the specified file in read mode, moves the cursor to the
    beginning of the file using seek, reads the entire content, and prints it.
    """

    with open(file_path, 'r') as file:
        file.seek(0)  # Move the cursor to the beginning of the file
        content = file.read()
        print("Content of the file:")
        print(content)
        


# Function to read a file without using fseek
def read_file_without_fseek(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        print("Content of the file:")
        print(content)

# Measure time taken to read the file using fseek
start_time = time.time()
read_file_with_fseek('sample.txt')
end_time = time.time()
print(f"Time taken to read file with fseek: {end_time - start_time:.6f} seconds")

# Measure time taken to read the file without using fseek
start_time = time.time()
read_file_without_fseek('sample.txt')
end_time = time.time()
print(f"Time taken to read file without fseek: {end_time - start_time:.6f} seconds")




# def main():
    
    
    
# if __name__ == "__main__":
#     main()