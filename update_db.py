import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users(
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
print("Database updated with profile fields!")