from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String())
    email = db.Column(db.String(), nullable = False, unique = True)
    password_hash = db.Column(db.String(), nullable = False)
    role = db.Column(db.String(), nullable = False)

class Genres(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    date_added = db.Column(db.Date(), nullable = False)
    books = db.relationship('Books')
    description = db.Column(db.String(), nullable = True, default = "There's no description for this genre")

class Books(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    author = db.Column(db.String(), nullable = False)
    genre = db.Column(db.Integer(), db.ForeignKey('genres.id'), nullable = False)
    description = db.Column(db.String(), nullable = True, default = "There's no description for this book")
    price = db.Column(db.Integer(), nullable = False)
    pdf_file = db.Column(db.String(), nullable = False)
    cover_pic = db.Column(db.String(), nullable = False)

class Requests(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'), nullable = False)

class Borrowings(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'), nullable = False)
    time = db.Column(db.DateTime(), nullable = False)

class AllBorrowings(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    book_name = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(), nullable=False)
    time = db.Column(db.DateTime(), nullable = False)

class Reviews(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    content = db.Column(db.String(), nullable = False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'), nullable = False)

class Purchases(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)
    book_id = db.Column(db.Integer(), db.ForeignKey('books.id'), nullable = False)



