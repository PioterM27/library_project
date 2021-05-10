from datetime import datetime

from flask import jsonify, request
from flask_login import login_required

from book_library_app import app
from book_library_app.models import Author
from book_library_app.utils import session_scope



@app.route('/api/v1/authors', methods=['GET'])
def get_authors():
    authors = Author.query
    list_of_authors = []
    for author in authors:
        list_of_authors.append(author.to_json())
    return jsonify({'status': 200, 'data': list_of_authors}),200



@app.route('/api/v1/authors/<int:author_id>', methods=['GET'])
def get_author(author_id: int):
    author = Author.query.filter(Author.id == author_id).one()
    return jsonify(author.to_json()),200


# obsluga POST ,z racji ze jest to metoda post to argument jest przegazany w requescie
@app.route('/api/v1/authors/<int:author_id>', methods=['PUT'])
@login_required
def update_author(author_id: int):
    try:
        author = Author.query.filter(Author.id == author_id).one()
    except Exception:
        message = f"Author with {author_id} not found"
        response_status = 404
    else:
        request_author = request.json
        # author.id = request_author["id"]
        author.first_name = request_author["first_name"]
        author.last_name = request_author["last_name"]
        author.birth_date = datetime.strptime(request_author["birth_date"], '%d-%m-%Y')
        message = "Author has been updated"
        response_status = 200
        with session_scope() as session:
            session
    return jsonify({
        "message": message,
        "status": response_status

    }), response_status


@app.route('/api/v1/authors', methods=['POST'])
@login_required
def create_authors():
    author = Author()
    request_author = request.json
    author.id = request_author["id"]
    author.first_name = request_author["first_name"]
    author.last_name = request_author["last_name"]
    author.birth_date = datetime.strptime(request_author["birth_date"], '%d-%m-%Y')
    with session_scope() as session:
        session.add(author)

    return jsonify({"status": 201, "info": "Author has been succesfful added"}), 201


@app.route('/api/v1/authors/<int:author_id>', methods=['DELETE'])
@login_required
def delete_author(author_id: int):
    author = Author.query.filter(Author.id == author_id).one()
    with session_scope() as session:
        session.delete(author)
    return jsonify({'status': 200, 'data': f'Author with id {author_id} has been deleted'}), 200
