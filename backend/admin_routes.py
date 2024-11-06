from flask import Blueprint, request, jsonify, send_file
from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, decode_token
from datetime import datetime, timedelta
from access_control import role_required
from tasks import *
from celery.result import AsyncResult
from caching import cache
from datetime import datetime
import os

admin = Blueprint("admin", __name__)

@admin.route("/admin/trial", methods = ["GET"])
def trial():
    bors = []
    for bor in AllBorrowings.query.all():
        bors.append(bor.time.month)
    print(bors)
    return "Hello"

# Admin Authentication
@admin.route("/admin/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return jsonify({"message": "Welcome to the Admin Registration Page"}), 200
    data = request.get_json()
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")
    password_hash = generate_password_hash(data.get("password"))
    role = "admin"

    if (Users.query.filter_by(email = email).first()):
        return jsonify({"message": "An Admin with this email already exists. Please enter a different one"}), 400
    
    new_admin = Users(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password_hash = password_hash,
        role = role)
    
    admin_info = {
        "admin_id": new_admin.id,
        "first_name": new_admin.first_name,
        "last_name": new_admin.last_name,
        "email": new_admin.email,
        "role": new_admin.role
    }
    
    access_token = create_access_token(identity = new_admin.id, expires_delta = timedelta(days = 15), additional_claims = {"role":"admin"})

    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({"message": "Registered Successfully", "access_token": access_token, "admin_info": admin_info}), 200

@admin.route("/admin/login", methods = ["POST", "GET"])
def login():
    if request.method == "GET":
        return jsonify({"message": "Welcome to the Admin Login Page"}), 200
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    admin = Users.query.filter_by(email = email, role = "admin").first()
    if not admin:
        return jsonify({"message": "An admin with this email does not exist"}), 400
    
    if not check_password_hash(admin.password_hash, password):
        return jsonify({"message": "Incorrect password"}), 400
    
    access_token = create_access_token(identity = admin.id, expires_delta = timedelta(days = 15), additional_claims = {"role":"admin"})

    admin_info = {
        "admin_id": admin.id,
        "first_name": admin.first_name,
        "last_name": admin.last_name,
        "email": admin.email,
        "role": admin.role
    }

    return jsonify({"message": "Logged in Successfully", "access_token": access_token, "admin_info": admin_info}), 200


# User Management 

@admin.route("/admin/get_users", methods = ["GET"])
@role_required("admin")
def get_users():
    users = []
    for user in Users.query.filter_by(role = "user").all():
        user_dict = {
            "id":user.id,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email
        }
        users.append(user_dict)
    return jsonify({"users":users}), 200


@admin.route("/admin/delete_user/<int:user_id>", methods = ["DELETE"])
@role_required("admin")
def delete_user(user_id):
    user = Users.query.filter_by(id = user_id).first()
    if not user:
        return jsonify({"msg":"This User Does Not Exist"}), 400
    
    for review in Reviews.query.filter_by(user_id=user_id):
        db.session.delete(review)
    for request in Requests.query.filter_by(user_id=user_id):
        db.session.delete(request)
    for borrowing in Borrowings.query.filter_by(user_id=user_id):
        db.session.delete(borrowing)

    db.session.delete(user)
    db.session.commit()

    users = []
    for user in Users.query.filter_by(role = "user").all():
        user_dict = {
            "id":user.id,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "email":user.email
        }
        users.append(user_dict)
    return jsonify({"msg":"Successfully Removed User", "users":users})

# Genre/Section Management

@admin.route("/admin/get_genres", methods = ["GET"])
@role_required("admin")
def get_genres():
    genres = []
    for genre in Genres.query.all():
        genres_dict = {
            "id":genre.id,
            "name":genre.name,
            "description":genre.description,
        }
        genres.append(genres_dict)
    return jsonify({"genres":genres}), 200


@admin.route("/admin/add_genre", methods = ["POST"])
@role_required("admin")
def add_genre(): 
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if Genres.query.filter_by(name = name).first():
        return jsonify({"msg":"This Genre Already Exists"}), 400
    
    new_genre = Genres(
        name = name,
        description = description,
        date_added = datetime.now()
    )

    db.session.add(new_genre)
    db.session.commit()

    genres = []
    for genre in Genres.query.all():
        genres_dict = {
            "id": genre.id,
            "name": genre.name,
            "description" :genre.description,
        }
        genres.append(genres_dict)

    return jsonify({"msg": "Genre Added Successfully", "genres":genres}), 201

@admin.route("/admin/delete_genre/<int:genre_id>", methods = ["DELETE"])
@role_required("admin")
def delete_genre(genre_id):
    genre = Genres.query.filter_by(id = genre_id).first()
    if not genre:
        return jsonify({"msg": "This Genre Doesn't Exist"}), 400

    if Books.query.filter_by(genre = genre_id).all():
        return jsonify({"msg": "There are books under this category, please edit their genres before continuing"}), 401

    db.session.delete(genre)
    db.session.commit()

    genres = []
    for genre in Genres.query.all():
        genres_dict = {
            "id":genre.id,
            "name":genre.name,
            "description":genre.description,
        }
        genres.append(genres_dict)
    return jsonify({"genres":genres, "msg": "Deleted Genre Successfully"}), 200


@admin.route("/admin/edit_genre/<int:genre_id>", methods = ["POST", "PUT"])
@role_required("admin")
def edit_genre(genre_id):
    data = request.get_json()
    genre = Genres.query.filter_by(id = genre_id).first()
    if not genre:
        return jsonify({"msg": "This Genre Doesn't Exist"}), 409
    
    if data.get("name"):
        genre.name = data.get("name")
    
    if data.get("description"):
        genre.description = data.get("description")
    
    db.session.commit()

    genres = []
    for genre in Genres.query.all():
        genres_dict = {
            "id":genre.id,
            "name":genre.name,
            "description":genre.description,
        }
        genres.append(genres_dict)

    return jsonify({"msg": "Edited Genre Successfully", "genres": genres}), 200


# Book Management

@admin.route("/admin/get_books", methods = ["GET"])
@role_required("admin")
def get_books():
    books = []
    for book in Books.query.all():
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
    
    genre_names = []
    for genre in Genres.query.all():
        genre_names.append(genre.name)
    
    return jsonify({"books": books, "genre_names": genre_names}), 200


@admin.route("/admin/add_book", methods = ["POST"])
@role_required("admin")
def add_book():
    pdf_file = request.files["pdf_file"]
    cover_pic = request.files["cover_pic"]
    name = request.form.get("name")
    author = request.form.get("author")
    genre = Genres.query.filter_by(name = request.form.get("genre")).first().id
    description = request.form.get("description")
    price = request.form.get("price")

    if Books.query.filter_by(name = name).first():
        return jsonify({"msg": "This Book Already Exists"}), 400
    
    # pdf_file_path = os.path.join("static/book_pdfs", pdf_file.filename)
    pdf_file.save(os.path.join("static/book_pdfs", pdf_file.filename))
    pdf_file_path = os.path.join("http://localhost:5000/static/book_pdfs", pdf_file.filename)

    # cover_pic_path = os.path.join("static/cover_pics", cover_pic.filename)
    cover_pic.save(os.path.join("static/cover_pics", cover_pic.filename))
    cover_pic_path = os.path.join("http://localhost:5000/static/cover_pics", cover_pic.filename)

    new_book = Books(
        name = name,
        author = author,
        genre = genre,
        description = description,
        price = price,
        pdf_file = pdf_file_path,
        cover_pic = cover_pic_path
    )

    db.session.add(new_book)
    db.session.commit()

    books = []
    for book in Books.query.all():
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
    
    genre_names = []
    for genre in Genres.query.all():
        genre_names.append(genre.name)
    
    return jsonify({"msg": "Book Added Successfully", "books": books}), 200


@admin.route("/admin/edit_book/<int:book_id>", methods = ["POST"])
@role_required("admin")
def edit_book(book_id):
    book = Books.query.filter_by(id = book_id).first()
    if not book:
        return jsonify({"msg": "This Book Doesn't Exist"}), 400

    if request.files:
        if request.files["pdf_file"]:
            pdf_file = request.files["pdf_file"]
            pdf_file_path = os.path.join("static/book_pdfs", pdf_file.filename)
            book.pdf_file = pdf_file_path

        if request.files["cover_pic"]:
            cover_pic = request.files["cover_pic"]
            cover_pic_path = os.path.join("static/cover_pics", cover_pic.filename)
            book.cover_pic = cover_pic_path

    if request.form.get("name"):
        book.name = request.form.get("name")
    if request.form.get("author"):
        book.author = request.form.get("author")
    if request.form.get("genre"):
        book.genre = Genres.query.filter_by(name = request.form.get("genre")).first().id
    if request.form.get("description"):
        book.description = request.form.get("description")
    if request.form.get("price"):
        book.price = request.form.get("price")
    
    db.session.commit()

    books = []
    for book in Books.query.all():
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
    
    return jsonify({"msg": "Edit Book Successfully", "books": books})
    

@admin.route("/admin/delete_book/<int:book_id>", methods = ["DELETE"])
@role_required("admin")
def delete_book(book_id):
    book = Books.query.filter_by(id = book_id).first()
    if not book:
        return jsonify({"msg": "This Book Doesn't Exist"}), 400
    
    for review in Reviews.query.filter_by(book_id=book_id).all():
        db.session.delete(review)
    
    # Check if any users have currently borrowed it
    if Borrowings.query.filter_by(book_id=book_id).all():
        return jsonify({"msg": "There are people who have borrowed this book. Please delete it later"}), 401

    for request in Requests.query.filter_by(book_id=book_id).all():
        db.session.delete(request)
    
    for review in Reviews.query.filter_by(book_id=book_id).all():
        db.session.delete(review)
    
    os.remove(os.path.join("static/book_pdfs", book.pdf_file.split("/")[-1]))
    os.remove(os.path.join("static/cover_pics", book.cover_pic.split("/")[-1]))

    db.session.delete(book)
    db.session.commit()

    books = []
    for book in Books.query.all():
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
    
    return jsonify({"msg": "Deleted Book Successfully", "books": books}), 200


# Manage Requests

@admin.route("/admin/get_requests", methods = ["GET"])
@role_required("admin")
def get_requests():
    requests = []
    for request in Requests.query.all():
        req_dict = {
            "id": request.id,
            "book_id": request.book_id,
            "book_name": Books.query.filter_by(id=request.book_id).first().name,
            "user_id": request.user_id
        }
        requests.append(req_dict)
    
    return jsonify({"requests": requests}), 200


@admin.route("/admin/approve_request/<int:request_id>", methods = ["GET"])
@role_required("admin")
def approve_request(request_id):
    request = Requests.query.get(request_id)

    new_borrowing = Borrowings(
        user_id=request.user_id,
        book_id=request.book_id,
        time=datetime.now()
    )

    new_past_borrowing = AllBorrowings(
        book_name=Books.query.filter_by(id=request.book_id).first().name,  
        genre=Genres.query.filter_by(id=Books.query.filter_by(id=request.book_id).first().genre).first().name,      
        time=datetime.now()
    )

    db.session.add(new_borrowing)
    db.session.add(new_past_borrowing)
    db.session.delete(request)
    db.session.commit()

    requests = []
    for request in Requests.query.all():
        req_dict = {
            "id": request.id,
            "book_id": request.book_id,
            "book_name": Books.query.filter_by(id=request.book_id).first().name,
            "user_id": request.user_id
        }
        requests.append(req_dict)
    
    return jsonify({"requests": requests, "msg": "Request Approved Successfully"}), 200
    

@admin.route("/admin/reject_request/<int:request_id>", methods = ["DELETE"])
@role_required("admin")
def reject_request(request_id):
    request = Requests.query.get(request_id)
    db.session.delete(request)
    db.session.commit()

    requests = []
    for request in Requests.query.all():
        req_dict = {
            "id": request.id,
            "book_id": request.book_id,
            "book_name": Books.query.filter_by(id=request.book_id).first().name,
            "user_id": request.user_id
        }
        requests.append(req_dict)
    
    return jsonify({"requests": requests, "msg": "Rejected Request Successfully"}), 200

#Manage Borrowings

@admin.route("/admin/get_borrowings", methods = ["GET"])
@role_required("admin")
def get_borrowings():
    borrowings = []
    for borrowing in Borrowings.query.all():
        bor_dict = {
            "id": borrowing.id,
            "user_id": borrowing.user_id,
            "book_id": borrowing.book_id,
            "book_name": Books.query.filter_by(id=borrowing.book_id).first().name,
            "time": borrowing.time,
            "expiry": borrowing.time + timedelta(days = 7)
        }
        borrowings.append(bor_dict)
    
    return jsonify({"borrowings": borrowings}), 200


@admin.route("/admin/revoke_access/<int:borrowing_id>", methods = ["DELETE"])
@role_required("admin")
def revoke_access(borrowing_id):
    borrowing = Borrowings.query.get(borrowing_id)
    db.session.delete(borrowing)
    db.session.commit()

    borrowings = []
    for borrowing in Borrowings.query.all():
        bor_dict = {
            "id": borrowing.id,
            "user_id": borrowing.user_id,
            "book_id": borrowing.book_id,
            "book_name": Books.query.filter_by(id=borrowing.book_id).first().name,
            "time": borrowing.time,
            "expiry": borrowing.time + timedelta(days = 7)
        }
        borrowings.append(bor_dict)
    
    return jsonify({"borrowings": borrowings, "msg": "Revoked Access Successfully"}), 200


@admin.route("/admin/generate_report", methods = ["GET"])
def generate_borrowing_report():
    task = generate_csv_report.delay()
    return jsonify({"taskID": task.id, "msg": "The report has started generating, please download it when it's ready"}), 200


@admin.route("/admin/download_report/<task_id>", methods = ["GET"])
def download_borrowing_report(task_id):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return send_file(os.path.join("static/reports", task_result.result))
    else:
        return jsonify({"msg": "The report isn't ready yet, please try again later"}), 404

@admin.route("/admin/send_email", methods = ["GET"])
def daily_reminder():
    reciever = "linus@proton.com"
    subject = "Reminder to Visit"
    content = """
    <h1>You Haven't Visited Opus in a While</h1>
    <p>Hi Linus, THANK YOU</p>
    """

    trigger_email(reciever, subject, content)

    return "Done", 200

