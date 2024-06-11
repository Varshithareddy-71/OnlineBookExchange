from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']
'''
engine = create_engine(
  db_connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })'''

engine = create_engine(db_connection_string)

def load_books_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from books"))
    books = []
    for row in result.all():
      books.append(dict(row))
    return books

def load_book_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM books WHERE id = :val"),
      val=id
    )
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0])


def add_order_to_db(book_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO book_order (book_id, full_name, email, phone, address) VALUES (:book_id, :full_name, :email, :phone, :address)")

    conn.execute(query, 
                 book_id=book_id, 
                 full_name=data['full_name'],
                 email=data['email'],
                 phone=data['phone'],
                 address=data['address'])