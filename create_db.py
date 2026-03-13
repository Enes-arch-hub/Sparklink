import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""

CREATE TABLE users(

id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
password TEXT,
age INTEGER,
gender TEXT,
location TEXT,
bio TEXT,
profile_photo TEXT

)

""")

conn.commit()

print("Users table created successfully")