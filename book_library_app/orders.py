from flask import jsonify, request,Response
from flask_login import login_required


from datetime import datetime, date, timedelta

from book_library_app import app
from book_library_app.models import User
from book_library_app.models import OrderBook
from book_library_app.models import Book
from book_library_app.utils import session_scope
from flask_login import login_required,login_user,logout_user,current_user

@app.route('/api/v1/orders', methods=['GET'])
def get_orders():
    pass

@app.route('/api/v1/orders/<int:book_id>', methods=['POST'])
def add_order(book_id):
    # user = User.query(User.id).filter(User.username == str(current_user.username)).one()
    user = User.query.filter(User.username == str(current_user.username)).one()
    print(user)
    book = Book.query.filter(Book.id == book_id).one()
    print("tutaj"+str(int(book_id)))
    print(book.available)
    # request_order = request.json
    print(datetime.utcnow())
    print(datetime.utcnow() + timedelta(days=14))
    if book.available:
        order = OrderBook()
        # order.id = 1
        order.book_id = int(book_id)
        order.user_id = int(user.id)
        order.title = book.title
        order.orders_date = datetime.utcnow()
        order.expired_date = datetime.utcnow() + timedelta(days=14)
        book.available = False
        with session_scope() as session:
            session.add(order)
    return jsonify({"status" : 201}), 201




