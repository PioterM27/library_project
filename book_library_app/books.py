'''zapytania  dla books'''
from flask import jsonify,request

from book_library_app import app, db
from book_library_app.models import Book, Author
from book_library_app.utils import session_scope



@app.route('/api/v1/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list=[]
    for book in books:
        book_list.append(book.to_json())
    return jsonify({
        'status': 200,
        'data': book_list
    }), 200


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    books = Book.query.filter(Book.id == book_id).one()
    return jsonify({"status": 200, "data":books.to_json()}), 200

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if not book:
        info = f"Book with {book_id} not found"
        return jsonify({"status": 404, "message": info}), 404
    else:
        request_book = request.json
        book.title = request_book["title"]
        book.isbn = request_book["isbn"]
        book.number_of_pages = request_book["number_of_pages"]
        description = request_book["description"]
        if description is not None:
            book.description = request_book["description"]
        message = "Book has been updated"
        with session_scope() as session:
            session

    return jsonify({"message": message})
@app.route('/api/v1/authors/<int:author_id>/books', methods=['POST'])
def create_book(author_id: int):
    author_verification = Author.query.filter(Author.id == author_id).first()
    if not author_verification:
        info = f"Author with id {author_id} not found"
        return jsonify({"status": 404, "message": info}), 404
    else:
        book = Book()
        request_book = request.json
        book.id = request_book["id"]
        book.title = request_book["title"]
        book.isbn = request_book["isbn"]
        book.number_of_pages = request_book["number_of_pages"]
        book.description = request_book["description"]
        book.author_id = request_book["author_id"]
        book.author = request_book["author"]
        with session_scope() as session:
            session.add(book)
        info = "Author has been succesfful added"

    return jsonify({"satus": 201, "info": info}), 201


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    book = Book.query.filter_by(id=book_id).one()
    with session_scope() as s:
        s.delete(book)
    return jsonify({'status': 200, 'data': f'Book with id {book_id} has been deleted'}), 200

@app.route('/api/v1/authors/<int:author_id>/books' , methods = ['GET'])
def get_all_author_books(author_id: int):
    author_verification = Author.query.filter(Author.id == author_id).first()
    if not author_verification:
        info = f"Author with id {author_id} not found"
        return jsonify({"status": 404,
                        "message": info}
        ), 404
    books = Book.query.filter(Book.author_id == author_id).all()
    book_list = []
    for book in books:
        book_list.append(book.to_json())
    return jsonify({
        'status': 200,
        'data': book_list,
        'number_of_records': len(books)

    }), 200


