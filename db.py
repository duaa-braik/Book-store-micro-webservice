import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE book(
    id integer PRIMARY KEY,
    title text NOT NULL,
    items integer NOT NULL,
    topic text NOT NULL,
    price integer NOT NULL
)                
"""


cursor.execute(sql_query)