import sqlite3

conn = sqlite3.connect("database.db")

# recreate likes table
conn.execute("DROP TABLE IF EXISTS likes")

conn.execute("""
CREATE TABLE likes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    liked_user_id INTEGER
)
""")

# recreate matches table
conn.execute("DROP TABLE IF EXISTS matches")

conn.execute("""
CREATE TABLE matches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user1_id INTEGER,
    user2_id INTEGER
)
""")

# recreate messages table
conn.execute("DROP TABLE IF EXISTS messages")

conn.execute("""
CREATE TABLE messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT
)
""")

conn.commit()

print("Database fixed successfully")