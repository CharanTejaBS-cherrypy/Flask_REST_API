# Books API

This is a simple RESTful API built with Flask and SQLite to manage a collection of books. The API allows you to perform CRUD operations (Create, Read, Update, Delete) on books stored in an SQLite database.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Code](#code)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CharanTejaBS-cherrypy/Flask_REST_API.git
   cd Flask_REST_API.git
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the SQLite database:

   ```bash
   python db.py
   ```

5. Run the Flask application:

   ```bash
   python app.py
   ```

The application will be available at `http://127.0.0.1:5000/`.

## Usage

### API Endpoints

#### Get All Books

- **URL:** `/books`
- **Method:** `GET`
- **Response:** JSON array of all books

  ```json
  [
      {
          "id": 1,
          "author": "Author Name",
          "language": "Language",
          "title": "Book Title"
      }
  ]
  ```

#### Add a New Book

- **URL:** `/books`
- **Method:** `POST`
- **Request Parameters:**
  - `author` (string): The author of the book
  - `language` (string): The language of the book
  - `title` (string): The title of the book
- **Response:** Confirmation message with the ID of the created book

  ```json
  {
      "message": "Book with the id: 1 created successfully"
  }
  ```

#### Get a Single Book

- **URL:** `/book/<id>`
- **Method:** `GET`
- **Response:** JSON object of the requested book

  ```json
  {
      "id": 1,
      "author": "Author Name",
      "language": "Language",
      "title": "Book Title"
  }
  ```

#### Update a Book

- **URL:** `/book/<id>`
- **Method:** `PUT`
- **Request Parameters:** (optional)
  - `author` (string): The new author of the book
  - `language` (string): The new language of the book
  - `title` (string): The new title of the book
- **Response:** JSON object of the updated book

  ```json
  {
      "id": 1,
      "author": "New Author",
      "language": "New Language",
      "title": "New Title"
  }
  ```

#### Delete a Book

- **URL:** `/book/<id>`
- **Method:** `DELETE`
- **Response:** Confirmation message

  ```json
  {
      "message": "The book with id: 1 has been DELETED!"
  }
  ```

## Database Schema

The SQLite database contains a single table `book` with the following schema:

- `id` (integer, primary key)
- `author` (text, not null)
- `language` (text, not null)
- `title` (text, not null)

## Code

### app.py

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

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
```

### db.py

```python
import sqlite3

conn = sqlite3.connect("books.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE book (id integer PRIMARY KEY, author text NOT NULL, language text NOT NULL, title text NOT NULL)"""

cursor.execute(sql_query)
```

### requirements.txt

```
blinker==1.8.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
gunicorn==22.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
packaging==24.1
Werkzeug==3.0.3
```

