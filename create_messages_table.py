import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""

CREATE TABLE IF NOT EXISTS messages(

id INTEGER PRIMARY KEY AUTOINCREMENT,
sender_id INTEGER,
receiver_id INTEGER,
message TEXT

)

""")

conn.commit()

print("Messages table created")