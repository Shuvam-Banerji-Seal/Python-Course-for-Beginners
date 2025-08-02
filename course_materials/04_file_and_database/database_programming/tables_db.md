
```python
import sqlite3

# Connect to SQLite database (creates one if it doesn't exist)
conn = sqlite3.connect('student.db')
cursor = conn.cursor()

# 1. Create a student table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    marks REAL
)
''')
print("Table created successfully.")

# 2. Insert data
students = [
    (1, 'Alice', 20, 85.5),
    (2, 'Bob', 22, 78.0),
    (3, 'Charlie', 21, 92.3),
    (4, 'David', 20, 69.4),
    (5, 'Eva', 23, 88.1)
]
cursor.executemany('INSERT OR IGNORE INTO student VALUES (?, ?, ?, ?)', students)
conn.commit()

# 3. ALTER TABLE to add a new attribute (email)
cursor.execute('ALTER TABLE student ADD COLUMN email TEXT')
print("Column 'email' added.")

# 4. UPDATE table to modify data
cursor.execute("UPDATE student SET email = 'alice@example.com' WHERE name = 'Alice'")
cursor.execute("UPDATE student SET email = 'bob@example.com' WHERE name = 'Bob'")
conn.commit()
print("Emails updated.")

# 5. ORDER BY - ascending
print("\nStudents ordered by marks (ascending):")
for row in cursor.execute("SELECT * FROM student ORDER BY marks ASC"):
    print(row)

# 6. ORDER BY - descending
print("\nStudents ordered by marks (descending):")
for row in cursor.execute("SELECT * FROM student ORDER BY marks DESC"):
    print(row)

# 7. DELETE a record
cursor.execute("DELETE FROM student WHERE name = 'David'")
conn.commit()
print("\nDeleted student 'David'.")

# 8. GROUP BY and aggregate functions (age-wise)
print("\nAggregate functions (grouped by age):")
for row in cursor.execute("""
SELECT age, COUNT(*), MIN(marks), MAX(marks), SUM(marks), AVG(marks)
FROM student
GROUP BY age
"""):
    print(f"Age: {row[0]}, Count: {row[1]}, Min: {row[2]}, Max: {row[3]}, Sum: {row[4]}, Avg: {row[5]:.2f}")

# Close connection
conn.close()
print("\nDatabase operations completed.")
```

---

### 📘 README.md

````markdown
# Student Database Management using SQLite and Python

This project demonstrates how to manage a `student` table using SQLite, integrated with Python via the built-in `sqlite3` module. The program creates a table, inserts data, and performs key SQL operations such as `ALTER`, `UPDATE`, `DELETE`, `ORDER BY`, and `GROUP BY`.

## 📁 Files

- `student_db.py`: Python script to manage and manipulate the `student` table.
- `student.db`: SQLite database generated after running the script.

## 💡 Features Implemented

### ✔ Table Creation

Creates a `student` table with:
- `id`: Primary key (INTEGER)
- `name`: Student name (TEXT)
- `age`: Student age (INTEGER)
- `marks`: Student marks (REAL)

### ✔ Data Insertion

Adds sample student data using `executemany`.

### ✔ ALTER TABLE

- Adds a new column `email` using `ALTER TABLE student ADD COLUMN email TEXT`.

### ✔ UPDATE

- Updates `email` for specific students.

### ✔ ORDER BY

- Displays students ordered by `marks` in both ascending and descending order.

### ✔ DELETE

- Deletes a student record (e.g., David).

### ✔ GROUP BY with Aggregate Functions

Performs aggregate queries grouped by `age`, including:
- `COUNT(*)`
- `MIN(marks)`
- `MAX(marks)`
- `SUM(marks)`
- `AVG(marks)`

## 🛠 Requirements

No external modules are required. This uses Python's built-in `sqlite3`.

```bash
python student_db.py
````

## 🧠 Learnings

* SQL table creation and manipulation.
* SQLite operations via Python.
* Integration of aggregate and conditional logic in SQL.
* Modifying database schema after creation.

## 📌 Notes

* The script uses `INSERT OR IGNORE` to avoid duplicate primary key errors.
* Make sure to delete the `student.db` file if you want a fresh start.

