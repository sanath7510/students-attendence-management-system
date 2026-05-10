import sqlite3

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
    usn TEXT PRIMARY KEY,
    name TEXT,
    department TEXT,
    semester TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usn TEXT,
    name TEXT,
    date TEXT,
    time TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database Ready")
