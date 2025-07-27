# import sys
# # lists_01= [1, 2, 3, 4, 5]

# # print(lists_01[0])  # Output: 1
# # print(lists_01[1])  # Output: 2 
# # print(f"the original lists_01 is {lists_01}")  # Output: the original lists_01 is [1, 2, 3, 4, 5]

# # # mutability of lists
# # lists_01[0] = 10
# # print(lists_01)  # Output: [10, 2, 3, 4, 5]
# # # lists_01[0] = 10
# # lists_01.append(10)
# # print(lists_01)  # Output: [10, 2, 3, 4, 5, 10]
# # # lists_01[0] = 10

# # #sets

# # sets_01 = {1, 2, 3, 4, 5}
# # print(sets_01)  # Output: {1, 2, 3, 4, 5}
# # print(f"the type of sets_01 is {type(sets_01)} \n The type of lists_01 is {type(lists_01)}")  # Output: the type of sets_01 is <class 'set'>
# # # mutability of sets
# # sets_01.add(6)
# # print(sets_01)  # Output: {1, 2, 3, 4, 5, 6}
# # sets_01.add(1)
# # print(sets_01)  # Output: {1, 2, 3, 4, 5, 6}

# # # print (sets_01[1]) # Output: TypeError: 'set' object is not subscriptable

# # # tuples
# # tuples_01 = (1, 2, 3, 4, 5)
# # print(tuples_01)  # Output: (1, 2, 3, 4, 5)
# # print(f"the type of tuples_01 is {type(tuples_01)} \n The type of lists_01 is {type(lists_01)}")        # Output: the type of tuples_01 is <class 'tuple'>
# # print(tuples_01[0])  # Output: 1
# # # tuples_01[0] = 10  # Output: TypeError: 'tuple' object does not support item assignment
# # # tuples are immutable objects in python
# # empty_listy = []
# # empty_sety = {}
# # empty_tuppy = ()
# # # print(f"the size of empty list {len(empty_listy)} \n the size of empty tuple {len(empty_tuppy)} \n the size of empty set : {len(empty_sety)}")  # Output: the size of tuples_01 is 5
# # print(f"the size of empty list {sys.getsizeof(empty_listy)} \n the size of empty tuple {sys.getsizeof(empty_tuppy)} \n the size of empty set : {sys.getsizeof(empty_sety)}")  # Output: the size of tuples_01 is 5

# # list slicing

# list01 = [1, 2, 3, 4, 5]
# print(list01[0:3])
# mixed_list = [1, 2, 3, 4, 5, "hello", True]
# print(mixed_list[0:3])
# # list_name[starting_index:ending_index:step] <-- syntax
# print(mixed_list[0:3:2])  # Output: [1, 3]
# print(mixed_list[::2])  # Output: [1, 3, 5, True]
# print(mixed_list[1:5:2])  # Output: [2, 4]
# print(mixed_list[1:5:3])  # Output: [2]

# ll2 = [20, 10, 30, 40, 50]
# print(mixed_list.extend(ll2))  # Output: None
# print(mixed_list)  # Output: [1, 2, 3, 4, 5, 'hello', True, 10, 20, 30, 40, 50]
# # print(sorted(mixed_list))
# print(mixed_list)  # Output: [10, 20, 30, 40, 50, 1, 2, 3, 4, 5, 'hello', True]
# print(sorted(ll2))


# # This sorting that we are doing is using "Quicksort algorithm" which is a divide and conquer algorithm
# # The time complexity of quicksort is O(nlogn) on average and O(n^2) in the worst case
# # The space complexity of quicksort is O(logn) on average and O(n) in the worst case

# print(reversed(ll2))  # Output: <list_reverseiterator object at 0x7f8c8c8c8c8>
# print(list(reversed(sorted(ll2))))  # Output: [50, 40, 30, 20, 10]

# ll2.append(30)
# print(ll2.count(30))  # Output: 2
# print(ll2.index(30))  # Output: 2
# print(ll2.pop())  # Output: 5
# print(ll2)  # Output: [20, 10, 30, 40, 50]

# print(ll2.insert(1, 100))  # Output: None
# print(ll2)  # Output: [20, 100, 10, 30, 40, 50]




# dictionaries in python
my_dictionary = {"name": "John", "age": 30, "city": "New York"}
print(type(my_dictionary))
print(type(my_dictionary["name"]))  # Output: John
my_dictionary["name"] = "Jane"
print(my_dictionary["name"])  # Output: Jane
my_dictionary.pop("name")
print(my_dictionary)  # Output: {'age': 30, 'city': 'New York'}
my_dictionary["name_01"] = "Jane"
print(my_dictionary)  # Output: {'age': 30, 'city': 'New York', 'name': 'Jane'}


#Nested dictionary
nested_dict = {
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY"
    }
}
print(nested_dict["address"]["city"])


def menu():
    print("1. Add item")
    print("2. Remove item")
    print("3. View items")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice


def main():
    items = []
    while True:
        choice = menu()
        if choice == "1":
            item = input("Enter item: ")
            items.append(item)
        elif choice == "2":
            item = input("Enter item: ")
            if item in items:
                items.remove(item)
            else:
                print("Item not found")
        elif choice == "3":
            print("Items: ", items)
        elif choice == "4":
            break
        else:
            print("Invalid choice")
            
if __name__ == "__main__":
    main()