# Tuple (Immutable)
my_tuple = (1, 2, 3)
print("Tuple:", my_tuple)

# List (Mutable)
my_list = [1, 2, 3]
print("List:", my_list)


# Accessing elements
print("First element of tuple:", my_tuple[0])
print("First element of list:", my_list[0])


# Attempt to modify a tuple (will raise an error)
try:
    my_tuple[0] = 1
except TypeError as e:
    print("Error:", e)

# Modify a list
my_list[0] = 10
print("Modified list:", my_list)



# Adding elements to a list
my_list.append(4)
print("List after append:", my_list)

# Tuples cannot be directly modified, but you can create a new tuple
new_tuple = my_tuple + (4,)
print("New tuple:", new_tuple)


print("Length of tuple:", len(my_tuple))
print("Length of list:", len(my_list))


print("Iterating through tuple:")
for item in my_tuple:
    print(item)

print("Iterating through list:")
for item in my_list:
    print(item)


print("Is 2 in tuple?", 2 in my_tuple)
print("Is 2 in list?", 2 in my_list)

#assignment 
x,y,z = 1,2,3
print(x,y,z)


a, b, c = my_tuple
print("Unpacked tuple values:", a, b, c)


# List operations
my_list.extend([5, 6])
print("List after extend:", my_list)

my_list.remove(10)  # Removes the first occurrence of 10
print("List after remove:", my_list)


# Tuples can be used as dictionary keys
my_dict = {my_tuple: "Tuple key"}
print("Dictionary with tuple key:", my_dict)

# Lists cannot be used as dictionary keys (will raise an error)
try:
    my_dict = {my_list: "List key"}
except TypeError as e:
    print("Error:", e)
