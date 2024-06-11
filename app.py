from flask import Flask, render_template, jsonify, request
from database import load_books_from_db, load_book_from_db, add_order_to_db

app = Flask(__name__)

@app.route("/")
def hello_jovian():
  books = load_books_from_db()
  return render_template('home.html', 
                         books=books)

@app.route("/api/books")
def list_books():
  books = load_books_from_db()
  return jsonify(books)

@app.route("/book/<id>")
def show_book(id):
  book = load_book_from_db(id)
  
  if not book:
    return "Not Found", 404
  
  return render_template('bookpage.html', 
                         book=book)

@app.route("/api/book/<id>")
def show_book_json(id):
  book = load_book_from_db(id)
  return jsonify(book)

@app.route("/book/<id>/buy", methods=['post'])
def buy_the_book(id):
  data = request.form
  book = load_book_from_db(id)
  add_order_to_db(id, data)
  return render_template('order_placed.html', 
                         book_order=data,
                         book=book)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)