import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("DROP TABLE IF EXISTS matches")

conn.execute("""

CREATE TABLE matches(

id INTEGER PRIMARY KEY AUTOINCREMENT,
user1_id INTEGER,
user2_id INTEGER

)

""")

conn.commit()

print("Matches table recreated successfully")