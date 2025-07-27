import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="shuvam",
    password="master",
    database="anime_universe"
)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS powers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    anime VARCHAR(100),
    technique VARCHAR(100),
    power_level INT
)
''')
conn.commit()

# Insert data using %s
sql = "INSERT INTO powers (name, anime, technique, power_level) VALUES (%s, %s, %s, %s)"
data = [
    ("Itachi", "Naruto", "Tsukuyomi", 9200),
    ("Saitama", "One Punch Man", "Serious Punch", 10000),
    ("Gojo", "Jujutsu Kaisen", "Infinity", 9800)
]
cursor.executemany(sql, data)
conn.commit()
print("Inserted rows:", cursor.rowcount)

# Update with .format()
new_power = 11000
name = "Saitama"
cursor.execute("UPDATE powers SET power_level = {} WHERE name = '{}'".format(new_power, name))
conn.commit()

# Display data
cursor.execute("SELECT * FROM powers")
for row in cursor.fetchall():
    print(row)

# Delete a row
cursor.execute("DELETE FROM powers WHERE name = %s", ("Itachi",))
conn.commit()
print("Deleted rows:", cursor.rowcount)

conn.close()
