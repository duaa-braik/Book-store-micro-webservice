import json
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the server'

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        searchData = request.data
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book where topic=?", (searchData.decode(),))
        books = [
            dict(id=row[0], title=row[1], items=row[2], topic=row[3], price=row[4])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)




########################################################################################        

@app.route('/info', methods=['POST', 'GET'])
def info():
    data = {}
    if request.method == 'GET':
        bookID = request.data
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book where id=?", (bookID.decode(),))
        books = cursor.fetchall()
        for book in books:
            data =  dict(id=book[0], title=book[1], items=book[2], topic=book[3], price=book[4])
        return data


######################################3


@app.route('/update', methods=['POST', 'GET'])
def update_data():
    bookID = request.data
    conn = db_connection()
    cursor = conn.cursor()
        
    cursor.execute("UPDATE book SET items=items-1 WHERE id=?", ( bookID.decode(),))
    conn.commit()
    cursor.execute("SELECT * FROM book where id=?", (bookID.decode(),))
    books = cursor.fetchall()
    for book in books:
        data =  dict(id=book[0], title=book[1], items=book[2], topic=book[3], price=book[4])
    return data





#####################################
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
        print('success')
    except sqlite3.error as e:
        print(e)
    return conn    
#####################################


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)