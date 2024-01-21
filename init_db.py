import sqlite3

connection = sqlite3.connect("flask_blog.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ("First post", "Content for first post (inserted via script).")
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ("Second post", "Content for second post (inserted via script).")
            )

cur.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
            ("test@test.com", "Test User", "P4$$w0rd")
            )

cur.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)",
            ("example@example.com", "Example User", "P4$$w0rd")
            )

connection.commit()
connection.close()
