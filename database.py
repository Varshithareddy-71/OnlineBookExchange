from sqlalchemy import create_engine, text
import os

'''db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(
  db_connection_string, 
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  })'''

engine = create_engine("mysql+pymysql://sql12712853:Flkd54ejDX@sql12.freesqldatabase.com/sql12712853?charset=utf8mb4")

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


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

    conn.execute(query, 
                 job_id=job_id, 
                 full_name=data['full_name'],
                 email=data['email'],
                 linkedin_url=data['linkedin_url'],
                 education=data['education'],
                 work_experience=data['work_experience'],
                 resume_url=data['resume_url'])