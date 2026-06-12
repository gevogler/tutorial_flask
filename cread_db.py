import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO posts (titulo, contenido) VALUES (?, ?)",
    ('Primera entrada', 'Contenido de la primera entrada: Hola mundo!')
)

cur.execute(
    "INSERT INTO posts (titulo, contenido) VALUES (?, ?)",
    ('Segunda entrada', 'Contenido de la segunda entrada: bla, bla')
)

connection.commit()
connection.close()