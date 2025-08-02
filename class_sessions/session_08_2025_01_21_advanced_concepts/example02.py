# Working with nested structures
school = {
    "class_A": {
        "teacher": "Mr. Smith",
        "students": ["John", "Emma"]
    },
    "class_B": {
        "teacher": "Mrs. Jones",
        "students": ["Alex", "Sarah"]
    }
}
print(school["class_A"]["teacher"])  # Output: Mr. Smith