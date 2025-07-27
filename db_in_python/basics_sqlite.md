 

## 📘 README: Python and SQL Database Interface (Anime Example)

This lesson demonstrates how to connect a Python program to an **SQLite** database using the `sqlite3` module. The example manages anime character data, showing how to insert, update, delete, and fetch data from the database.

---

### 🔧 File: `sqlite_anime_example.py`

```python
import sqlite3
```

* **What it does:** Imports Python’s built-in SQLite interface.
* **Behind the scenes:** Loads the `_sqlite3` C extension module, which wraps the SQLite embedded database engine.

---

```python
conn = sqlite3.connect("anime_characters.db")
```

* **What it does:** Opens a connection to a database file named `anime_characters.db`. If the file doesn’t exist, it creates one.
* **Function call detail:** Internally, `sqlite3.connect()` calls `_sqlite3.connect()` from the C extension. It returns a `Connection` object.
* **conn object:** Represents the open connection to the database and allows you to perform transactions.

---

```python
cursor = conn.cursor()
```

* **What it does:** Creates a **cursor** object to interact with the database.
* **Function call detail:** Calls the `cursor()` method of the `Connection` object. Returns a `Cursor` object.
* **cursor object:** Acts like a "command executor" that prepares and runs SQL statements and stores query results.

---

```python
cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    anime TEXT,
    power_level INTEGER
)
''')
```

* **What it does:** Executes a SQL query to create a table (if not already exists) with four columns.
* **Function call detail:** `Cursor.execute()` calls a lower-level `_sqlite3_stmt` object to prepare and run SQL.

---

```python
conn.commit()
```

* **What it does:** Commits (saves) the current transaction to the database.
* **Why needed:** Without `commit()`, changes like `INSERT`, `UPDATE`, or `DELETE` are kept in memory only.
* **Function call detail:** Internally runs the SQLite command `COMMIT`.

---

```python
characters = [
    ("Goku", "Dragon Ball", 9000),
    ("Naruto", "Naruto", 8500),
    ("Luffy", "One Piece", 8700)
]
```

* **What it does:** Prepares a list of character records as tuples.
* **Use:** Ideal for `executemany()`.

---

```python
cursor.executemany("INSERT INTO characters (name, anime, power_level) VALUES (?, ?, ?)", characters)
```

* **What it does:** Inserts all three characters in one call.
* **Placeholders `?`:** Safely injects data using parameterized queries (prevents SQL injection).
* **Function call detail:** Loops internally over the list, preparing and executing the SQL statement for each tuple.

---

```python
conn.commit()
```

* **What it does:** Saves the inserts to disk.

---

```python
cursor.execute("UPDATE characters SET power_level = 9500 WHERE name = 'Goku'")
```

* **What it does:** Updates Goku's power level.
* **Behind the scenes:** Compiles the SQL string to a SQLite bytecode statement, then executes it.

---

```python
print(f"Updated rows: {cursor.rowcount}")
```

* **What it does:** Prints how many rows were affected.
* **Note:** Not all database engines update `rowcount` reliably; SQLite usually does.

---

```python
cursor.execute("DELETE FROM characters WHERE name = 'Naruto'")
print(f"Deleted rows: {cursor.rowcount}")
```

* **What it does:** Deletes the Naruto row and prints the row count.
* **DELETE statement:** Executes via the same SQL bytecode mechanism internally.

---

```python
cursor.execute("SELECT * FROM characters")
rows = cursor.fetchall()
```

* **`fetchall()`:** Retrieves all results as a list of tuples.
* **Internal mechanism:** The `Cursor` keeps an internal pointer to the result set and iterates through it.

---

```python
for row in rows:
    print(row)
```

* **What it does:** Displays each row (id, name, anime, power\_level).

---

```python
cursor.execute("SELECT name FROM characters WHERE id = 1")
print("Single fetch:", cursor.fetchone())
```

* **`fetchone()`:** Fetches only the first row of the result.
* **Memory-efficient:** Useful when you expect a single result or large data sets.

---

```python
conn.close()
```

* **What it does:** Closes the database connection.
* **Why important:** Frees resources like file handles and memory buffers.

---

## 🧪 Recap of Key Functions

| Function        | Role                                       |
| --------------- | ------------------------------------------ |
| `connect()`     | Opens a connection to an SQLite DB file    |
| `cursor()`      | Returns a cursor object for SQL execution  |
| `execute()`     | Runs a single SQL statement                |
| `executemany()` | Runs many SQL statements with one template |
| `commit()`      | Saves all pending transactions             |
| `fetchone()`    | Gets the next single row of the result set |
| `fetchall()`    | Gets all remaining rows of the result set  |
| `rowcount`      | Returns the number of affected rows        |
| `close()`       | Closes the database connection             |

---

## 📌 Notes on Internal Behavior

* **SQLite engine:** Compiles SQL to a bytecode and executes it in a small virtual machine.
* **Python DB-API 2.0:** `sqlite3` complies with this interface standard (PEP 249).
* **Cursor state:** Maintains internal state during fetches; resets on new `execute()`.

---

## 👾 Anime Use Case Examples

* Use power levels to sort or filter characters.
* Add episodes watched per character and join with another table.
* Create a separate table for **anime series** and perform joins.

