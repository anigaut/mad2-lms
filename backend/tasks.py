from celery import shared_task
from flask_excel import make_response_from_array
from datetime import datetime, timedelta
from models import *
from mailhog_config import *
from jinja2 import Template


@shared_task()
def generate_csv_report():
    borrowings = [("Book Name", "Genre", "Date Borrowed")]
    for bor in AllBorrowings.query.all():
        borrowings.append((bor.book_name, bor.genre, bor.time))

    csv_output = make_response_from_array(array=borrowings, file_type="csv")
    
    # Define the file name
    filename = f"borrowing_report_{datetime.now().day}-{datetime.now().month}-{datetime.now().year}.csv"
    
    # Open the file in write-binary mode
    with open(f"./static/reports/{filename}", 'wb') as file:
        file.write(csv_output.data)
    
    return filename


@shared_task(ignore_result=True)
def daily_reminder():
    for borrowing in Borrowings.query.all():
        user_email = Users.query.filter_by(id=borrowing.user_id).first().email
        user_first_name = Users.query.filter_by(id=borrowing.user_id).first().first_name
        book_name = Books.query.filter_by(id=borrowing.book_id).first().name
        time_left = (borrowing.time + timedelta(days=7)).day - borrowing.time.day

        to = user_email
        subject = "Reminder To Return Book"
        content_body = f"""
        <p>Hi {user_first_name},<p>
        <div>This is to inform you that your borrowing of the book {book_name} will expire in {time_left} days. Please return the book before the due date.</div>
        <br>
        <p>Regards, Opus Team</p>
        """

        send_email(to, subject, content_body)
    return None

@shared_task(ignore_result=True)
def monthly_report(month):
    bors = []
    for borrowing in AllBorrowings.query.all():
        if borrowing.time.month == month:
            bors.append(borrowing)
    
    content_body = f"""
    <p>Dear Admin,</p>
    <br>
    <div>Please find below data pertaining to all the borrowings that were made by users during this month.</div>
    <br>
    <table border='1' style='border-collapse:collapse'>
        <tr>
            <th>Book Name</th>
            <th>Genre</th>
            <th>Time of Borrowing</th>
        </tr>
    """

    for bor in bors:
        row = f"""
        <tr>
            <td>{bor.book_name}</td>
            <td>{bor.genre}</td>
            <td>{bor.time}</td>
        </tr>
        """
        content_body += row
    content_body += "</table>"

    send_email("anirudhg@opus.com", "Monthly Report", content_body)
    return None

