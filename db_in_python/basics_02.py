import sqlite3

# Connect to SQLite (creates file if not exists)
conn = sqlite3.connect("anime_characters.db")
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    anime TEXT,
    power_level INTEGER
)
''')
conn.commit()

# Insert records
characters = [
    ("Goku", "Dragon Ball", 9000),
    ("Naruto", "Naruto", 8500),
    ("Luffy", "One Piece", 8700)
]

cursor.executemany("INSERT INTO characters (name, anime, power_level) VALUES (?, ?, ?)", characters)
conn.commit()

# Update power level
cursor.execute("UPDATE characters SET power_level = 9500 WHERE name = 'Goku'")
print(f"Updated rows: {cursor.rowcount}")
conn.commit()

# Delete a record
cursor.execute("DELETE FROM characters WHERE name = 'Naruto'")
print(f"Deleted rows: {cursor.rowcount}")
conn.commit()

# Select and display all records
cursor.execute("SELECT * FROM characters")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Fetch one
cursor.execute("SELECT name FROM characters WHERE id = 1")
print("Single fetch:", cursor.fetchone())

conn.close()
