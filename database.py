from pymysql import cursors
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql
import os

my_secret = os.environ['DB_CONNECTION_STRING']
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="mysqldbproj-varshithareddy1901-1e6e.d.aivencloud.com",
  password=my_secret,
  read_timeout=timeout,
  port=14070,
  user="avnadmin",
  write_timeout=timeout,
)

def load_books_from_db():
  connection.ping()
  with connection.cursor() as cursor :
    cursor.execute("select * from books")
    books = []
    for row in cursor.fetchall():
     books.append(dict(row))
  connection.commit()
  return books


def load_user_books_from_db(userid):
  connection.ping()
  with connection.cursor() as cursor :
    cursor.execute("select * from books where ownerid=%s", userid )
    books = []
    for row in cursor.fetchall():
     books.append(dict(row))
  connection.commit()
  return books


def load_book_from_db(id):
  connection.ping()
  with connection.cursor() as cursor :
    cursor.execute("SELECT * FROM books WHERE id = %s", id )
    rows = cursor.fetchall()
  connection.commit()
  if len(rows) == 0:
    return None
  else:
    return dict(rows[0])


def add_book_to_db(title, author, price, about, category, ownerid) :
  connection.ping()
  with connection.cursor() as cursor :
    query = "INSERT INTO books (title, author, price, about, category, ownerid) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (title, author, price, about, category, ownerid))
  connection.commit()


def add_order_to_db(book_id, full_name, email, phone, address):
  connection.ping()
  with connection.cursor() as cursor :
    query = "INSERT INTO book_order (book_id, full_name, email, phone, address) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (book_id, full_name, email, phone, address))
  connection.commit()


def add_user_to_db(name, email, password) :
  connection.ping()
  with connection.cursor() as cursor :
    query = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, 
                 (name, email, password))
  connection.commit()


def load_user_from_db(username) :
  connection.ping()
  with connection.cursor() as cursor :
    cursor.execute("SELECT * FROM user WHERE name = %s", username)
    rows = cursor.fetchall()
  connection.commit()
  if len(rows) == 0:
    return None
  else:
    return dict(rows[0])


def load_order_of_userbook(userid) :
  connection.ping()
  with connection.cursor() as cursor :
    cursor.execute("SELECT books.title, books.author,books.price, book_order.full_name, book_order.email, book_order.address, book_order.phone FROM books INNER JOIN book_order ON books.id = book_order.book_id and books.ownerid=%s ;", userid )
    orders = []
    for row in cursor.fetchall():
     orders.append(dict(row))
  connection.commit()
  return orders

def load_owner_from_db(ownerid) :
  connection.ping()
  with connection.cursor() as cursor :
    cursor.execute("SELECT * FROM user WHERE userid = %s", ownerid)
    rows = cursor.fetchall()
  connection.commit()
  if len(rows) == 0:
    return None
  else:
    return dict(rows[0])