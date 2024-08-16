from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from database import load_books_from_db, load_book_from_db, add_book_to_db, add_order_to_db, add_user_to_db, load_user_from_db, load_owner_from_db, load_user_books_from_db, load_order_of_userbook, load_namedbooks_from_db, delete_book_from_db, load_user_wishlist, add_book_to_wishlist, delete_book_from_wishlist
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import smtplib
import os

app = Flask(__name__)
app.secret_key = 'a_b_c_d_e_f'
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def my_book_exchange():
  books = load_books_from_db()
  return render_template('home.html', 
                         books=books)

@app.route("/<userid>")
def user_page(userid):
    books = load_books_from_db()
    return render_template('userhome.html', 
                            books=books,userid=userid)
    
@app.route("/api/books")
def list_books():
  books = load_books_from_db()
  return jsonify(books)

@app.route("/<userid>/book/<id>")
def show_book(id,userid):
  book = load_book_from_db(id)
  
  if not book:
    return "Not Found", 404
  
  return render_template('bookpage.html',userid=userid, 
                         book=book)

@app.route("/api/book/<id>")
def show_book_json(id):
  book = load_book_from_db(id)
  return jsonify(book)

@app.route("/<userid>/search", methods=['GET', 'POST'])
def search_book(userid) :
    book= request.form
    books=load_namedbooks_from_db(book.get('book_name'))
    if len(books)==0 :
        return render_template('book_to_wishlist.html', userid=userid)
    return render_template('search.html', books=books, userid=userid)

@app.route("/<userid>/book/<id>/buy", methods=['post'])
def buy_the_book(id,userid):
  data = request.form
  book = load_book_from_db(id)
  add_order_to_db(id, data.get('full_name'), data.get('email'), data.get('phone'), data.get('address'))
  
  owner=load_owner_from_db(book['ownerid'])
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login("varshithareddy1901@gmail.com", "kinaxovugdayccmp")
  message = "Dear "+owner['name']+",\n\n"+"You have a new order for the book "+book['title']+"\n\n"+"Please find the details below:\n\n"+"Full Name: "+data.get('full_name')+"\n\n"+"Email: "+data.get('email')+"\n\n"+"Phone: "+data.get('phone')+"\n\n"+"Address: "+data.get('address')+ "\n\n"+"Thank you."
  s.sendmail("varshithareddy1901@gmail.com", owner['email'], message)
  s.quit()
  return render_template('order_placed.html',userid=userid, 
                         book_order=data,
                         book=book)

@app.route("/<userid>/addbook")
def enter_book_details(userid):
  return render_template('add_book.html', 
                         userid=userid)
    
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/<userid>/booksadded", methods=['post'])
def add_the_book(userid) :
    data = request.form
    if 'file' not in request.files or 'back' not in request.files :
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    back = request.files['back']
    if file.filename == '' or back.filename == '' :
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename) and back and allowed_file(back.filename) :
        filename = secure_filename(file.filename)
        filename2 = secure_filename(back.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        back.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        add_book_to_db(data.get('title'), data.get('author'), data.get('price'), data.get('about'), data.get('category'), userid, filename, filename2)
        books1 = load_user_books_from_db(userid)
        return render_template('book_added.html', books=books1, userid=userid)    
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route("/<userid>/mybooks")
def my_books(userid) :
    books1 = load_user_books_from_db(userid)
    return render_template('book_added.html', books=books1, userid=userid)

@app.route("/<userid>/mybookorders")
def my_book_orders(userid) :
    orders=load_order_of_userbook(userid)   
    return render_template('book_orders.html',orders=orders, userid=userid)

@app.route("/<userid>/<id>/delete")
def delete_book(userid,id) :
    delete_book_from_db(id)
    return redirect(url_for('my_book_orders',userid=userid))

@app.route("/<userid>/bookToWishlist")
def book_details(userid):
  return render_template('book_to_wishlist.html', 
                         userid=userid)

@app.route("/<userid>/addedToWishlist", methods=['post'])
def added_to_wishlist(userid) :
    data = request.form
    add_book_to_wishlist(data.get('title'), data.get('author'), data.get('category'), userid)
    return redirect(url_for('wishlist', userid=userid ))

@app.route("/<userid>/wishlist")
def wishlist(userid) :
    wish=load_user_wishlist(userid)
    avail={}
    books=[]
    for w in wish :
        books.extend(load_namedbooks_from_db(w['title']))
        if(len(books)==0) :
            avail[w['id']]="Not Available"
        else :
            avail[w['id']]="Available"
        books.clear()
    return render_template('wishlist.html', userid=userid, books=wish, availability=avail)

@app.route("/<userid>/<id>/deletewish")
def delete_from_wishlist(userid,id) :
    delete_book_from_wishlist(id)
    return redirect(url_for('wishlist',userid=userid))

@app.route('/signup', methods=['GET', 'POST'])
def signup() :
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        add_user_to_db(username, email, hashed_password)

        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user=load_user_from_db(username)

        if check_password_hash(user['password'], password):
            session['user_id'] = user['userid']
            session['username'] = user['name']
            return redirect(url_for('profile'))
        else:
            flash('Login failed! Check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        f"Welcome {session['username']}!"
        return redirect(url_for('user_page',userid=session['user_id']))
    else:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return my_book_exchange()


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)