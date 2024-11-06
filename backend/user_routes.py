from flask import Blueprint, request, jsonify
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request, get_jwt
from caching import cache
from datetime import datetime, timedelta
from access_control import role_required
import json

user = Blueprint("user", __name__)

def groups_of(l, n):
  groups = []
  for i in range(0, len(l), n):
    groups.append(l[i:i+n])
  return groups


@user.route("/user/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return jsonify({"message": "Welcome to the User Registration Page"}), 200
    data = request.get_json()
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    password_hash = generate_password_hash(data.get("password"))
    role = "user"
    
    if (Users.query.filter_by(email = email).first()):
        return jsonify({"message": "A User with this email already exists. Please enter a different one"}), 400
    
    new_user = Users(
        first_name = first_name, 
        last_name = last_name, 
        email = email, 
        password_hash = password_hash, 
        role = role)
    
    user_info = {
        "user_id": Users.query.all()[-1].id + 1,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "role": new_user.role
    }
    
    access_token = create_access_token(identity = new_user.id, expires_delta = timedelta(days = 15), additional_claims = {"role":"user"})
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registered Successfully", "access_token": access_token, "user_info": user_info}), 200


@user.route("/user/login", methods = ["POST", "GET"])
def login():
    if request.method == "GET":
        return jsonify({"message": "Welcome to the User Login Page"}), 200
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = Users.query.filter_by(email = email, role = "user").first()

    if not user:
        return jsonify({"message": "User with this email does not exist"}), 400
    
    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Incorrect Password"}), 400
    
    access_token = create_access_token(identity = user.id, expires_delta = timedelta(days = 15), additional_claims = {"role":"user"})

    user_info = {
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role
    }

    return jsonify({"message": "Logged in Successfully", "access_token": access_token, "user_info": user_info}), 200

@user.route("user/logout", methods = ["POST"])
@role_required("user")
def logout():
    response = jsonify({"msg": "Logged Out Successfully"})
    unset_jwt_cookies(response)
    return response, 200
    

@user.route("/user/home", methods = ["GET"])
@cache.cached(timeout=30)
def home():
    books = []
    for book in Books.query.all()[:8]:
        genre = Genres.query.filter_by(id = book.genre).first().name
        book_dict = {
            "id": book.id,
            "name": book.name,
            "genre": genre,
            "author": book.author,
            "description": book.description,
            "price": book.price,
            "pdf_file": book.pdf_file,
            "cover_pic": book.cover_pic
        }
        books.append(book_dict)
    books = groups_of(books, 4)

    return jsonify({"books": books}), 200


@user.route("/user/search/<query>", methods = ["GET"])
@cache.cached(timeout=10)
def search(query):
    books = []
    for book in Books.query.filter(Books.name.contains(query)).all():
        genre = Genres.query.filter_by(id = book.genre).first().name
        book_dict = {
            "id": book.id,
            "name": book.name,
            "genre": genre,
            "author": book.author,
            "description": book.description,
            "price": book.price,
            "pdf_file": book.pdf_file,
            "cover_pic": book.cover_pic
        }
        books.append(book_dict)
    books = groups_of(books, 4)

    genres = []
    for genre in Genres.query.filter(Genres.name.contains(query)).all():
        genres_dict = {
            "id":genre.id,
            "name":genre.name,
            "description":genre.description,
        }
        genres.append(genres_dict)
    genres = groups_of(genres, 4)

    books_by_author = []
    for book in Books.query.filter(Books.author.contains(query)).all():
        genre = Genres.query.filter_by(id = book.genre).first().name
        book_dict = {
            "id": book.id,
            "name": book.name,
            "genre": genre,
            "author": book.author,
            "description": book.description,
            "price": book.price,
            "pdf_file": book.pdf_file,
            "cover_pic": book.cover_pic
        }
        books_by_author.append(book_dict)
    books_by_author = groups_of(books_by_author, 4)

    return jsonify({"books": books, "genres": genres, "books_by_author": books_by_author}), 200

@user.route("/user/browse", methods = ["GET"])
@cache.cached(timeout=10)
def browse():
    genres = []
    for genre in Genres.query.all():
        genres_dict = {
            "id":genre.id,
            "name":genre.name,
            "description":genre.description,
        }
        genres.append(genres_dict)
    genres = groups_of(genres, 4)

    return jsonify({"genres": genres}), 200


@user.route("/user/browse/<int:genre_id>", methods = ["GET"])
def browse_by_genre(genre_id):
    books = []
    for book in Books.query.filter_by(genre = genre_id).all():
        genre = Genres.query.filter_by(id = book.genre).first().name
        book_dict = {
            "id": book.id,
            "name": book.name,
            "genre": genre,
            "author": book.author,
            "description": book.description,
            "price": book.price,
            "pdf_file": book.pdf_file,
            "cover_pic": book.cover_pic
        }
        books.append(book_dict)
    books = groups_of(books, 4)
    return jsonify({"books": books}), 200


@user.route("/user/book_details/<int:book_id>", methods = ["GET"])
@role_required("user")
def get_book_details(book_id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    print(user_id)

    book_object = Books.query.filter_by(id = book_id).first()
    genre = Genres.query.filter_by(id = book_object.genre).first().name
    book = {
        "id": book_object.id,
        "name": book_object.name,
        "genre": genre,
        "author": book_object.author,
        "description": book_object.description,
        "price": book_object.price,
        "pdf_file": book_object.pdf_file,
        "cover_pic": book_object.cover_pic
    }

    reviews = []
    for review in Reviews.query.filter_by(book_id = book_id).all():
        reviewer_first_name = Users.query.filter_by(id = review.user_id).first().first_name
        reviewer_last_name = Users.query.filter_by(id = review.user_id).first().last_name

        rev_dict = {
            "content": review.content,
            "user_first_name": reviewer_first_name,
            "user_last_name": reviewer_last_name,
            "book_id": review.book_id
        }
        reviews.append(rev_dict)
    
    currently_borrowed = True if Borrowings.query.filter_by(user_id=user_id, book_id=book_id).first() else False

    purchased = True if Purchases.query.filter_by(user_id=user_id, book_id=book_id).first() else False

    return jsonify({"book": book, "reviews": reviews, "currently_borrowed": currently_borrowed, "purchased": purchased}), 200

@user.route("/user/request_book/<int:book_id>", methods = ["GET"])
@role_required("user")
def request_book(book_id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    print(user_id)

    if Requests.query.filter_by(user_id=user_id, book_id=book_id).first():
        return jsonify({"msg": "You have already requested to borrow this book. Pleae wait till an admin approves your request"}), 403
    
    if len(Borrowings.query.filter_by(user_id=user_id).all()) + len(Requests.query.filter_by(user_id=user_id).all()) >= 5:
        return jsonify({"msg": "You can borrow a maximum of 5 books at a time"}), 403
    
    new_request = Requests(
        user_id=user_id,
        book_id=book_id
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({"msg": "Request has been made. Please wait till an admin approves it"}), 200


@user.route("/user/return_book/<int:book_id>", methods = ["DELETE"])
@role_required("user")
def return_book(book_id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    print(user_id)

    borrowing = Borrowings.query.filter_by(book_id=book_id, user_id=user_id).first()

    if not borrowing:
        return jsonify({"msg": "You have not borrowed this book"}), 404
    
    db.session.delete(borrowing)
    db.session.commit()

    return jsonify({"msg": "The book has been returned"}), 200


@user.route("/user/purchase_book/<int:book_id>", methods = ["GET"])
@role_required("user")
def purchase_book(book_id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()

    if Purchases.query.filter_by(user_id=user_id, book_id=book_id).first():
        return jsonify({"msg": "You have already purchased this book"}), 401
    
    new_purchase = Purchases(
        user_id=user_id,
        book_id=book_id
    )

    db.session.add(new_purchase)
    db.session.commit()

    return jsonify({"msg": "You have bought the book, you may now read it anytime"}), 200


@user.route("/user/add_review", methods = ["POST"])
@role_required("user")
def add_review():
    content = request.get_json().get("content")
    user_id = request.get_json().get("user_id")
    book_id = request.get_json().get("book_id")

    new_review = Reviews(
        content=content,
        user_id=user_id,
        book_id=book_id
    )

    db.session.add(new_review)
    db.session.commit()

    reviews = []
    for review in Reviews.query.filter_by(book_id=book_id).all():
        reviewer_first_name = Users.query.filter_by(id = review.user_id).first().first_name
        reviewer_last_name = Users.query.filter_by(id = review.user_id).first().last_name
        rev_dict = {
            "content": review.content,
            "user_first_name": reviewer_first_name,
            "user_last_name": reviewer_last_name,
            "book_id": review.book_id
        }
        reviews.append(rev_dict)
    
    return jsonify({"reviews": reviews}), 200


@user.route("/user/read_book/<int:book_id>", methods = ["GET"])
@role_required("user")
def read_book(book_id):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    print(user_id, book_id)
    borrowed = Borrowings.query.filter_by(user_id=user_id, book_id = book_id).first()
    purchased = Purchases.query.filter_by(user_id=user_id, book_id = book_id).first()
    if not (borrowed or purchased):
        return jsonify({"msg": "You have not borrowed or purchased this book"}), 403

    book_object = Books.query.filter_by(id = book_id).first()
    genre = Genres.query.filter_by(id = book_object.genre).first().name
    book = {
        "id": book_object.id,
        "name": book_object.name,
        "genre": genre,
        "author": book_object.author,
        "description": book_object.description,
        "price": book_object.price,
        "pdf_file": book_object.pdf_file,
        "cover_pic": book_object.cover_pic
    }

    return jsonify({"book":book}), 200