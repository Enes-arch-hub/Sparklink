import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""

CREATE TABLE IF NOT EXISTS likes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
liker_id INTEGER,
liked_id INTEGER

)

""")

conn.commit()

print("Likes table created")