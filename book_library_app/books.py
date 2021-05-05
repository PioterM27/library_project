'''zapytania  dla books'''

from flask import jsonify,request
from book_library_app import app, db
from book_library_app.models import Book, Author



@app.route('/api/v1/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list=[]
    for book in books:
        book_list.append(book.to_json())
    return jsonify({
        'success': True,
        'data': book_list
    })


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int):
    books = Book.query.filter(Book.id == book_id).one()
    return jsonify(books.to_json())

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id: int):
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if not book:
        message = f"Book with {book_id} not found"
    else:
        request_book = request.json
        book.title = request_book["title"]
        book.isbn = request_book["isbn"]
        book.number_of_pages = request_book["number_of_pages"]
        description = request_book["description"]
        if description is not None:
            book.description = request_book["description"]
        message = "Book has been updated"
        db.session.commit()

    return jsonify({"message": message})
@app.route('/api/v1/authors/<int:author_id>/books', methods=['POST'])
def create_book(author_id: int):
    author_verification = Author.query.filter(Author.id == author_id).first()
    if not author_verification:
        info = f"Author with id {author_id} not found"
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
        db.session.add(book)
        db.session.commit()
        info = "Author has been succesfful added"

    return jsonify({"succes": True, "info": info})


@app.route('/api/v1/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    book = Book.query.filter_by(id=book_id).one()
    db.session.delete(book)
    db.session.commit()
    return jsonify({'success': True, 'data': f'Book with id {book_id} has been deleted'})

@app.route('/api/v1/authors/<int:author_id>/books' , methods = ['GET'])
def get_all_author_books(author_id: int):
    author_verification = Author.query.filter(Author.id == author_id).first()
    if not author_verification:
        info = f"Author with id {author_id} not found"
    books = Book.query.filter(Book.author_id == author_id).all()
    book_list = []
    for book in books:
        book_list.append(book.to_json())
    return jsonify({
        'success' : True,
        'data' : book_list,
        'number_of_records' : len(books)

    })


