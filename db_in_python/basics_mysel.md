
# Database in Python
## 📘 README: Python and MySQL Interface with Anime-Themed Examples

This script demonstrates how to connect Python to a **MySQL database** using the `mysql.connector` module and execute basic SQL operations: `INSERT`, `UPDATE`, `DELETE`, and `SELECT`.

The examples use anime characters and their special techniques to make learning more engaging.

---

### 🔧 File: `mysql_anime_example.py`

---

### 🔁 Setup Requirements

Before running the script:

1. Install MySQL server and create a database:

   ```sql
   CREATE DATABASE anime_universe;
   ```

2. Install Python MySQL connector:

   ```bash
   pip install mysql-connector-python
   ```

---

### 🔍 Code Breakdown

```python
import mysql.connector
```

* **What it does:** Imports the `mysql.connector` library to interact with MySQL.
* **Behind the scenes:** Internally uses `CMySQLConnection` class that wraps the MySQL C client library.

---

```python
conn = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="anime_universe"
)
```

* **Purpose:** Establishes a connection to the MySQL server.
* **Returns:** A `MySQLConnection` object.
* **Under the hood:** Sends a TCP/IP request to the MySQL server, negotiates authentication, and initializes session state.

---

```python
cursor = conn.cursor()
```

* **Purpose:** Creates a cursor object used to execute SQL commands.
* **Details:** The `cursor()` method returns a `MySQLCursor` object that maintains context for queries and result sets.

---

```python
cursor.execute('''
CREATE TABLE IF NOT EXISTS powers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    anime VARCHAR(100),
    technique VARCHAR(100),
    power_level INT
)
''')
```

* **Purpose:** Creates the `powers` table with columns for anime character data.
* **AUTO\_INCREMENT:** Automatically generates unique `id` values.

---

```python
conn.commit()
```

* **Purpose:** Confirms the creation of the table by committing the transaction.
* **Why important:** In MySQL, `CREATE TABLE` is DDL and implicitly commits, but it’s still good practice to call `commit()` for consistency.

---

```python
sql = "INSERT INTO powers (name, anime, technique, power_level) VALUES (%s, %s, %s, %s)"
data = [
    ("Itachi", "Naruto", "Tsukuyomi", 9200),
    ("Saitama", "One Punch Man", "Serious Punch", 10000),
    ("Gojo", "Jujutsu Kaisen", "Infinity", 9800)
]
```

* **%s Placeholders:** Used for safe parameter substitution (avoids SQL injection).
* **Why `%s` and not `?`:** The MySQL connector uses `%s` as the standard placeholder, even for integers.

---

```python
cursor.executemany(sql, data)
```

* **Purpose:** Efficiently inserts multiple rows into the table.
* **Internal mechanics:** Compiles one SQL statement and binds each set of values in the list sequentially.

---

```python
conn.commit()
print("Inserted rows:", cursor.rowcount)
```

* **rowcount:** Number of rows successfully inserted.

---

```python
new_power = 11000
name = "Saitama"
cursor.execute("UPDATE powers SET power_level = {} WHERE name = '{}'".format(new_power, name))
```

* **Purpose:** Updates Saitama’s power level using `.format()`.
* ⚠️ **Security Warning:** `.format()` is less safe — do **not** use with untrusted input. Use parameterized queries (`%s`) instead in real applications.

---

```python
conn.commit()
```

* **Commits the change** to the database.

---

```python
cursor.execute("SELECT * FROM powers")
for row in cursor.fetchall():
    print(row)
```

* **fetchall():** Retrieves all rows in the result set.
* **Internal behavior:** The `MySQLCursor` fetches all records into memory, returns them as a list of tuples.

---

```python
cursor.execute("DELETE FROM powers WHERE name = %s", ("Itachi",))
```

* **Safe Deletion:** Uses `%s` to safely pass parameters.

---

```python
conn.commit()
print("Deleted rows:", cursor.rowcount)
```

* **rowcount:** Tells you how many rows were affected.

---

```python
conn.close()
```

* **Purpose:** Closes the connection to the MySQL server.
* **Why important:** Frees up server-side resources like threads, memory buffers, and file handles.

---

## 🧠 Recap of Key Functions

| Function        | Description                                     |
| --------------- | ----------------------------------------------- |
| `connect()`     | Connects to the MySQL server                    |
| `cursor()`      | Prepares a cursor for query execution           |
| `execute()`     | Executes a single SQL command                   |
| `executemany()` | Executes the same SQL command for multiple rows |
| `commit()`      | Saves all pending database changes              |
| `fetchone()`    | Gets the first row from the result set          |
| `fetchall()`    | Gets all rows from the result set               |
| `rowcount`      | Number of rows affected by the last operation   |
| `close()`       | Closes the database connection                  |

---

## 🌌 Anime-Inspired Ideas for Further Exploration

* Add columns for "affiliation" or "villain/hero" type
* Add a second table for "anime\_series" and JOIN on `anime`
* Build a leaderboard sorted by `power_level`
* Filter results based on power ranges (e.g., > 9000)

---

## 🚨 Security Note on `.format()`

Using `.format()` in SQL queries **can lead to SQL injection** if the input comes from an untrusted source. Always prefer:

```python
cursor.execute("SELECT * FROM powers WHERE name = %s", ("Saitama",))
```

over

```python
cursor.execute("SELECT * FROM powers WHERE name = '{}'".format(user_input))
```


