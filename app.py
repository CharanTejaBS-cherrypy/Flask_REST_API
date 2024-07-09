from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


# @app.route('/')
# def index():
#     return "Hello World!"


# @app.route('/<name>')
# def print_name(name):
#     return "Welcome, {}".format(name)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, language, title) VALUES (?, ?, ?)"""
        cursor = conn.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something Wrong", 404

    if request.method == 'PUT':
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r

        if book is None:
            return "Book not found", 404

        author = request.form.get('author', book[1])
        language = request.form.get('language', book[2])
        title = request.form.get('title', book[3])
        
        sql = """ UPDATE book SET title=?, author=?, language=? WHERE id=? """
        conn.execute(sql, (title, author, language, id))
        conn.commit()
        
        updated_book = {
            'id': id,
            'author': author,
            'language': language,
            'title': title
        }
        return jsonify(updated_book), 200

    if request.method == 'DELETE':
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been DELETED!".format(id), 200


if __name__ == '__main__':
    app.run(debug=True)
