import sqlite3

conn = sqlite3.connect('hogwarts.db')
cur = conn.cursor()

# Create tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        year INTEGER NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        grade TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    );
""")
# Insert into table (inserts one row)
cur.execute("INSERT INTO students (name, year) VALUES (?, ?)", ("Harry Potter", 5))


conn.commit()
conn.close()

#Then when querying the db you can use this code:

uri = f'file:hogwarts.db?mode=ro'
db_conn = sqlite3.connect(uri, uri=True)
cursor = db_conn.cursor()

cursor.execute(query)

rows = cursor.fetchall()
db_conn.close()
